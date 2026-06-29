from fastapi.testclient import TestClient

from signalpay_api.app import app, payment_events, reset_state


def client() -> TestClient:
    reset_state()
    return TestClient(app)


def auth(token: str = "sp_live_payments_capture") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_get_payment_returns_contract_shape() -> None:
    response = client().get("/payments/pay_1001", headers=auth("sp_live_payments_reader"))

    assert response.status_code == 200
    assert response.json() == {
        "paymentId": "pay_1001",
        "customerId": "cus_9001",
        "amount": 12500,
        "currency": "USD",
        "status": "authorized",
    }


def test_capture_requires_an_idempotency_key() -> None:
    response = client().post("/payments/pay_1001/capture", headers=auth())

    assert response.status_code == 400
    assert response.json()["detail"] == "Idempotency-Key header is required"


def test_capture_is_idempotent_and_emits_one_event() -> None:
    api = client()
    headers = auth() | {"Idempotency-Key": "cap-pay-1001-001"}

    first = api.post("/payments/pay_1001/capture", headers=headers)
    second = api.post("/payments/pay_1001/capture", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["status"] == "captured"
    assert len(payment_events) == 1
    assert payment_events[0]["customerId"] == "cus_9001"
    assert payment_events[0]["type"] == "payment.captured"


def test_capture_requires_capture_scope() -> None:
    response = client().post(
        "/payments/pay_1001/capture",
        headers=auth("sp_live_payments_reader") | {"Idempotency-Key": "cap-denied-001"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "payments:capture scope is required"


def test_rejects_sessions_for_other_token_families() -> None:
    response = client().get(
        "/payments/pay_1001",
        headers=auth("sp_live_settlement_reader"),
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "session token is not valid for audience payments-api"


def refund_auth(token: str = "sp_live_payments_refund") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_refund_requires_an_idempotency_key() -> None:
    response = client().post("/payments/pay_1001/refund", headers=refund_auth())

    assert response.status_code == 400
    assert response.json()["detail"] == "Idempotency-Key header is required"


def test_refund_requires_refund_scope() -> None:
    api = client()
    headers = auth("sp_live_payments_reader") | {"Idempotency-Key": "ref-denied-001"}

    response = api.post("/payments/pay_1001/refund", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "payments:refund scope is required"
    assert len(payment_events) == 0


def test_refund_transitions_captured_to_refunded() -> None:
    api = client()
    # First capture the payment so it can be refunded
    api.post(
        "/payments/pay_1001/capture",
        headers=auth() | {"Idempotency-Key": "cap-for-refund-001"},
    )
    payment_events.clear()

    headers = refund_auth() | {"Idempotency-Key": "ref-pay-1001-001"}
    response = api.post("/payments/pay_1001/refund", headers=headers)

    assert response.status_code == 200
    assert response.json()["status"] == "refunded"
    assert response.json()["paymentId"] == "pay_1001"
    assert len(payment_events) == 1
    assert payment_events[0]["type"] == "payment.refunded"
    assert payment_events[0]["customerId"] == "cus_9001"


def test_refund_is_idempotent_and_emits_one_event() -> None:
    api = client()
    api.post(
        "/payments/pay_1001/capture",
        headers=auth() | {"Idempotency-Key": "cap-for-refund-002"},
    )
    payment_events.clear()

    headers = refund_auth() | {"Idempotency-Key": "ref-pay-1001-002"}
    first = api.post("/payments/pay_1001/refund", headers=headers)
    second = api.post("/payments/pay_1001/refund", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert len(payment_events) == 1


def test_refund_rejects_non_captured_payment() -> None:
    api = client()
    headers = refund_auth() | {"Idempotency-Key": "ref-pay-1001-003"}

    response = api.post("/payments/pay_1001/refund", headers=headers)

    assert response.status_code == 409
    assert "captured" in response.json()["detail"]
