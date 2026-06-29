from __future__ import annotations

from fastapi.testclient import TestClient

from signalpay_api.app import app, payment_events, reset_state

client = TestClient(app)


def auth(token: str = "sp_live_payments_refund") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_refund_requires_idempotency_key() -> None:
    reset_state()

    response = client.post("/payments/pay_1001/refund", headers=auth())

    assert response.status_code == 400
    assert response.json()["detail"] == "Idempotency-Key header is required"


def test_refund_is_idempotent_and_emits_one_event() -> None:
    reset_state()
    headers = auth() | {"Idempotency-Key": "refund-demo-1"}

    first = client.post("/payments/pay_1001/refund", headers=headers)
    second = client.post("/payments/pay_1001/refund", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["status"] == "refunded"
    assert len(payment_events) == 1
    assert payment_events[0]["type"] == "payment.refunded"
