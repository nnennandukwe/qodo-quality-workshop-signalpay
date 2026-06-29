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


def refund_auth() -> dict[str, str]:
    return auth("sp_live_payments_refund")


def capture_pay_1001(api: TestClient) -> None:
    response = api.post(
        "/payments/pay_1001/capture",
        headers=auth("sp_live_payments_capture") | {"Idempotency-Key": "cap-setup-001"},
    )
    assert response.status_code == 200


def refund_events() -> list[dict]:
    return [event for event in payment_events if event["type"] == "payment.refunded"]


def test_refund_captured_payment_emits_one_refund_event() -> None:
    api = client()
    capture_pay_1001(api)

    response = api.post(
        "/payments/pay_1001/refund",
        headers=refund_auth() | {"Idempotency-Key": "ref-pay-1001-001"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "paymentId": "pay_1001",
        "customerId": "cus_9001",
        "amount": 12500,
        "currency": "USD",
        "status": "refunded",
    }
    assert refund_events() == [
        {
            "eventId": "payment.refunded:pay_1001",
            "type": "payment.refunded",
            "paymentId": "pay_1001",
            "customerId": "cus_9001",
            "amount": 12500,
            "currency": "USD",
            "status": "refunded",
        }
    ]


def test_refund_is_idempotent_on_retry() -> None:
    api = client()
    capture_pay_1001(api)
    headers = refund_auth() | {"Idempotency-Key": "ref-pay-1001-retry"}

    first = api.post("/payments/pay_1001/refund", headers=headers)
    second = api.post("/payments/pay_1001/refund", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert len(refund_events()) == 1


def test_refund_requires_an_idempotency_key() -> None:
    api = client()
    capture_pay_1001(api)

    response = api.post("/payments/pay_1001/refund", headers=refund_auth())

    assert response.status_code == 400
    assert response.json()["detail"] == "Idempotency-Key header is required"
    assert refund_events() == []


def test_refund_requires_refund_scope() -> None:
    api = client()
    capture_pay_1001(api)

    response = api.post(
        "/payments/pay_1001/refund",
        headers=auth("sp_live_payments_reader") | {"Idempotency-Key": "ref-denied-001"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "payments:refund scope is required"
    assert refund_events() == []
    state = api.get("/payments/pay_1001", headers=auth("sp_live_payments_reader"))
    assert state.json()["status"] == "captured"


def test_refund_rejects_non_captured_payment() -> None:
    api = client()

    response = api.post(
        "/payments/pay_1002/refund",
        headers=refund_auth() | {"Idempotency-Key": "ref-pay-1002-001"},
    )

    assert response.status_code == 409
    assert refund_events() == []
    state = api.get("/payments/pay_1002", headers=auth("sp_live_payments_reader"))
    assert state.json()["status"] == "pending"


def test_refund_unknown_payment_returns_404() -> None:
    response = client().post(
        "/payments/pay_unknown/refund",
        headers=refund_auth() | {"Idempotency-Key": "ref-unknown-001"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "payment not found"
    assert refund_events() == []


def test_refund_rejects_wrong_audience() -> None:
    response = client().post(
        "/payments/pay_1001/refund",
        headers=auth("sp_live_settlement_reader") | {"Idempotency-Key": "ref-aud-001"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "session token is not valid for audience payments-api"
