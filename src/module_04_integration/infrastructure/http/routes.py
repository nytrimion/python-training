import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...domain.event_dispatcher import EventDispatcher
from ...domain.events import AccountCreatedEvent
from ...domain.job_dispatcher import JobDispatcher
from ..dependencies import (
    get_event_dispatcher,
    get_job_dispatcher,
)

router = APIRouter()


class AccountCreationRequest(BaseModel):
    """Account creation request."""
    email: str


class AccountCreationResponse(BaseModel):
    """Account creation response."""
    account_id: str
    status: str
    message: str
    verification_job_id: str


@router.post("/accounts", response_model=AccountCreationResponse)
async def create_account(
        request: AccountCreationRequest,
        event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
        job_dispatcher: JobDispatcher = Depends(get_job_dispatcher),
) -> AccountCreationResponse:
    """
    Create a new account.

    The account verification email is sent asynchronously by a job worker.
    The tracking of the new account is handled by event.
    """
    account_id = str(uuid.uuid7())
    created_event = AccountCreatedEvent(
        account_id=account_id,
        email=request.email,
    )
    event_dispatcher.dispatch(created_event)
    verification_job = job_dispatcher.dispatch("verify_account_email", created_event)

    return AccountCreationResponse(
        account_id=account_id,
        status="pending",
        message="Account verification pending",
        verification_job_id=verification_job.id,
    )
