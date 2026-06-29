from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
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

_IDEMPOTENCY_STORE_PATH = Path(
    ".signalpay_idempotency_store.json"
)


def _load_idempotency_results() -> dict[str, dict[str, Any]]:
    """Load idempotency results from durable storage.

    This repository uses a file-backed store to keep the workshop API
    self-contained while preventing duplicate side effects across process
    restarts.
    """

    try:
        data = json.loads(_IDEMPOTENCY_STORE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    results: dict[str, dict[str, Any]] = {}
    for key, value in data.items():
        if isinstance(key, str) and isinstance(value, dict):
            results[key] = value
    return results


def _persist_idempotency_results(results: dict[str, dict[str, Any]]) -> None:
    """Persist idempotency results to durable storage."""

    tmp_path = _IDEMPOTENCY_STORE_PATH.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    tmp_path.replace(_IDEMPOTENCY_STORE_PATH)


idempotency_results: dict[str, dict[str, Any]] = _load_idempotency_results()

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
    """Capture an authorized payment.

    Uses an idempotency key to ensure a single capture event is emitted per key.
    """

    require_principal(authorization, required_scope="payments:capture")
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="payment not found")

    result_key = f"capture:{payment_id}:{idempotency_key}"
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
    _persist_idempotency_results(idempotency_results)
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
    """Refund a captured payment.

    Enforces idempotency via a durable store and emits a single
    `payment.refunded` event on the first successful request.
    """

    require_principal(authorization, required_scope="payments:refund")
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    if payment_id not in payments:
        raise HTTPException(status_code=404, detail="payment not found")

    result_key = f"refund:{payment_id}:{idempotency_key}"
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
    _persist_idempotency_results(idempotency_results)
    return payment
