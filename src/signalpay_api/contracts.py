from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict

PaymentStatus = Literal["authorized", "pending", "captured", "failed", "refunded"]
PaymentEventType = Literal["payment.captured", "payment.refunded"]


class PaymentEvent(TypedDict):
    eventId: str
    type: PaymentEventType
    paymentId: str
    customerId: str
    amount: int
    currency: str
    status: PaymentStatus


@dataclass(frozen=True)
class Principal:
    subject: str
    audience: str
    scopes: tuple[str, ...]


TOKENS: dict[str, Principal] = {
    "sp_live_payments_reader": Principal(
        subject="support-reader",
        audience="payments-api",
        scopes=("payments:read",),
    ),
    "sp_live_payments_capture": Principal(
        subject="capture-operator",
        audience="payments-api",
        scopes=("payments:read", "payments:capture"),
    ),
    "sp_live_payments_refund": Principal(
        subject="refund-operator",
        audience="payments-api",
        scopes=("payments:read", "payments:refund"),
    ),
    "sp_live_settlement_reader": Principal(
        subject="settlement-reader",
        audience="settlement-worker",
        scopes=("settlement:read",),
    ),
}


def verify_session(token: str, audience: str) -> Principal:
    """Return the principal for a known workshop token."""
    try:
        principal = TOKENS[token]
    except KeyError as exc:
        raise ValueError("unknown session token") from exc

    if principal.audience != audience:
        raise ValueError(f"session token is not valid for audience {audience}")
    return principal


def build_payment_event(
    *,
    event_type: PaymentEventType,
    payment_id: str,
    customer_id: str,
    amount: int,
    currency: str,
    status: PaymentStatus,
) -> PaymentEvent:
    """Build the stable event shape consumed by downstream payment systems."""
    return {
        "eventId": f"{event_type}:{payment_id}",
        "type": event_type,
        "paymentId": payment_id,
        "customerId": customer_id,
        "amount": amount,
        "currency": currency,
        "status": status,
    }
