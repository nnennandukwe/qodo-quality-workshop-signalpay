import pytest

from signalpay_api.contracts import build_payment_event, verify_session


def test_verify_session_returns_expected_scope() -> None:
    principal = verify_session("sp_live_payments_refund", "payments-api")

    assert principal.subject == "refund-operator"
    assert "payments:refund" in principal.scopes


def test_verify_session_rejects_wrong_audience() -> None:
    with pytest.raises(ValueError, match="session token is not valid"):
        verify_session("sp_live_settlement_reader", "payments-api")


def test_build_payment_event_uses_stable_contract_shape() -> None:
    event = build_payment_event(
        event_type="payment.captured",
        payment_id="pay_1001",
        customer_id="cus_9001",
        amount=12500,
        currency="USD",
        status="captured",
    )

    assert event == {
        "eventId": "payment.captured:pay_1001",
        "type": "payment.captured",
        "paymentId": "pay_1001",
        "customerId": "cus_9001",
        "amount": 12500,
        "currency": "USD",
        "status": "captured",
    }
