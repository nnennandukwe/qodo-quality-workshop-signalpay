from __future__ import annotations

from copy import deepcopy
from typing import Annotated, Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from signalpay_api.contracts import PaymentStatus, build_payment_event, verify_session


class Payment(BaseModel):
    payment_id: str = Field(alias="paymentId")
    customer_id: str = Field(alias="customerId")
    amount: int
    currency: str
    status: PaymentStatus

    model_config = {"populate_by_name": True}


INITIAL_PAYMENTS: dict[str, dict[str, Any]] = {
    "pay_1001": {
        "paymentId": "pay_1001",
        "customerId": "cus_9001",
        "amount": 12500,
        "currency": "USD",
        "status": "authorized",
    },
    "pay_1002": {
        "paymentId": "pay_1002",
        "customerId": "cus_9002",
        "amount": 4900,
        "currency": "USD",
        "status": "pending",
    },
}

payments: dict[str, dict[str, Any]] = deepcopy(INITIAL_PAYMENTS)
payment_events: list[dict[str, Any]] = []
idempotency_results: dict[tuple[str, str, str], dict[str, Any]] = {}

app = FastAPI(
    title="SignalPay Payments API",
    summary="Self-contained payments API for the Qodo quality-first workshop.",
    description=(
        "Use this API through `/docs` to practice planning, Qodo rules, "
        "local verification gates, PR review, and remediation."
    ),
)


def reset_state() -> None:
    """Reset in-memory state for tests and local workshop retries."""
    payments.clear()
    payments.update(deepcopy(INITIAL_PAYMENTS))
    payment_events.clear()
    idempotency_results.clear()


def require_principal(
    authorization: str | None,
    *,
    required_scope: str | None = None,
) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer session token is required")

    token = authorization.removeprefix("Bearer ").strip()
    try:
        principal = verify_session(token, "payments-api")
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    if required_scope and required_scope not in principal.scopes:
        raise HTTPException(
            status_code=403,
            detail=f"{required_scope} scope is required",
        )


@app.get("/payments/{payment_id}", response_model=Payment, response_model_by_alias=True)
def get_payment(
    payment_id: str,
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> dict[str, Any]:
    require_principal(authorization)
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="payment not found")
    return payments[payment_id]


@app.post("/payments/{payment_id}/capture", response_model=Payment, response_model_by_alias=True)
def capture_payment(
    payment_id: str,
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
    idempotency_key: Annotated[
        str | None,
        Header(alias="Idempotency-Key"),
    ] = None,
) -> dict[str, Any]:
    require_principal(authorization, required_scope="payments:capture")
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="payment not found")

    result_key = ("capture", payment_id, idempotency_key)
    if result_key in idempotency_results:
        return idempotency_results[result_key]

    payment = payments[payment_id]
    payment["status"] = "captured"

    event = build_payment_event(
        event_type="payment.captured",
        payment_id=payment["paymentId"],
        customer_id=payment["customerId"],
        amount=payment["amount"],
        currency=payment["currency"],
        status="captured",
    )
    payment_events.append(dict(event))
    idempotency_results[result_key] = deepcopy(payment)
    return payment


@app.post("/payments/{payment_id}/refund", response_model=Payment, response_model_by_alias=True)
def refund_payment(
    payment_id: str,
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
    idempotency_key: Annotated[
        str | None,
        Header(alias="Idempotency-Key"),
    ] = None,
) -> dict[str, Any]:
    require_principal(authorization, required_scope="payments:refund")
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="payment not found")

    result_key = ("refund", payment_id, idempotency_key)
    if result_key in idempotency_results:
        return idempotency_results[result_key]

    payment = payments[payment_id]
    if payment["status"] != "captured":
        raise HTTPException(status_code=409, detail="payment must be captured before refund")

    payment["status"] = "refunded"

    event = build_payment_event(
        event_type="payment.refunded",
        payment_id=payment["paymentId"],
        customer_id=payment["customerId"],
        amount=payment["amount"],
        currency=payment["currency"],
        status="refunded",
    )
    payment_events.append(dict(event))
    idempotency_results[result_key] = deepcopy(payment)
    return payment
