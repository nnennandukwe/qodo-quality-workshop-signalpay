from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Annotated, Any, cast

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
_IDEMPOTENCY_STORE_PATH = Path(".signalpay_idempotency_store.json")


def idempotency_result_key(operation: str, payment_id: str, idempotency_key: str) -> str:
    """Build the durable lookup key for a payment mutation result."""
    return json.dumps((operation, payment_id, idempotency_key), separators=(",", ":"))


def load_idempotency_results() -> dict[str, dict[str, Any]]:
    """Load durable idempotency results from the local workshop store."""
    try:
        data: object = json.loads(_IDEMPOTENCY_STORE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    results: dict[str, dict[str, Any]] = {}
    for key, value in cast(dict[object, object], data).items():
        if isinstance(key, str) and isinstance(value, dict):
            stored_result = cast(dict[str, Any], value)
            results[key] = deepcopy(stored_result)
    return results


def persist_idempotency_results() -> None:
    """Persist idempotency results to a durable local file."""
    tmp_path = _IDEMPOTENCY_STORE_PATH.with_suffix(".tmp")
    tmp_path.write_text(
        json.dumps(idempotency_results, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    tmp_path.replace(_IDEMPOTENCY_STORE_PATH)


idempotency_results: dict[str, dict[str, Any]] = load_idempotency_results()

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
    try:
        _IDEMPOTENCY_STORE_PATH.unlink()
    except FileNotFoundError:
        pass


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
    """Capture a payment once per operation-specific idempotency key."""
    require_principal(authorization, required_scope="payments:capture")
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="payment not found")

    result_key = idempotency_result_key("capture", payment_id, idempotency_key)
    if result_key in idempotency_results:
        return idempotency_results[result_key]

    payment = payments[payment_id]
    if payment["status"] == "refunded":
        raise HTTPException(status_code=409, detail="cannot capture a refunded payment")

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
    persist_idempotency_results()
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
    """Refund a captured payment once per operation-specific idempotency key."""
    require_principal(authorization, required_scope="payments:refund")
    if idempotency_key is None or idempotency_key == "":
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="payment not found")

    result_key = idempotency_result_key("refund", payment_id, idempotency_key)
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
    persist_idempotency_results()
    return payment
