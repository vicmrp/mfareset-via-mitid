import logging
from typing import Any

from core.models import MFAResetEvent, MitIDLoginEvent
from core.utils.auth_methods import (
    sanitize_prepared_auth_method,
    sanitize_raw_auth_method,
)

logger = logging.getLogger(__name__)


def normalize_username(username: str) -> str:
    normalized = username.strip().lower()
    if "@" not in normalized:
        normalized = f"{normalized}@dtu.dk"
    return normalized


def get_request_metadata(request: Any) -> dict[str, Any]:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "").strip()
    ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else ""

    if not ip_address:
        ip_address = request.META.get("REMOTE_ADDR", "").strip()

    session_key = ""
    if getattr(request, "session", None) is not None:
        session_key = request.session.session_key or ""

    return {
        "ip_address": ip_address or None,
        "user_agent": request.META.get("HTTP_USER_AGENT", "")[:1000],
        "session_key": session_key,
    }


def log_mitid_login_success(
    *,
    request: Any,
    username: str,
    service_url: str = "",
) -> None:
    try:
        MitIDLoginEvent.objects.create(
            username=normalize_username(username),
            status=MitIDLoginEvent.STATUS_SUCCESS,
            service_url=service_url,
            ticket_present=bool(request.GET.get("ticket")),
            **get_request_metadata(request),
        )
    except Exception:
        logger.exception("Failed to persist MitID login success audit event")


def log_mitid_login_failure(
    *,
    request: Any,
    failure_reason: str,
    service_url: str = "",
    username: str = "",
) -> None:
    try:
        MitIDLoginEvent.objects.create(
            username=normalize_username(username) if username else "",
            status=MitIDLoginEvent.STATUS_FAILURE,
            service_url=service_url,
            failure_reason=failure_reason,
            ticket_present=bool(request.GET.get("ticket")),
            **get_request_metadata(request),
        )
    except Exception:
        logger.exception("Failed to persist MitID login failure audit event")


def log_mfa_reset_event(
    *,
    request: Any,
    username: str,
    status: str,
    attempted_methods: list[dict[str, Any]] | None = None,
    existing_methods: list[dict[str, Any]] | None = None,
    result_message: str = "",
    failure_reason: str = "",
) -> None:
    try:
        MFAResetEvent.objects.create(
            username=normalize_username(username),
            status=status,
            attempted_methods=[
                sanitize_prepared_auth_method(method)
                for method in (attempted_methods or [])
            ],
            existing_methods=[
                sanitize_raw_auth_method(method)
                for method in (existing_methods or [])
            ],
            result_message=result_message,
            failure_reason=failure_reason,
            **get_request_metadata(request),
        )
    except Exception:
        logger.exception("Failed to persist MFA reset audit event")
