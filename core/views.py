import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from django_cas_ng.views import LoginView as CASLoginView

from core.utils.audit import (
    log_mfa_reset_event,
    log_mitid_login_failure,
    normalize_username,
)
from core.utils.auth_methods import prepare_auth_methods
from core.utils.graph import list_user_authentication_methods
from core.utils.reset_mfa import reset_mfa_methods

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "core/home.html")


@login_required
def profile(request):
    attributes = request.session.get("attributes", {})
    auth_methods = []
    graph_error = None
    username = normalize_username(request.user.username)

    try:
        raw_methods = list_user_authentication_methods(username)
        auth_methods = prepare_auth_methods(raw_methods)
    except Exception:
        logger.exception("Failed to fetch authentication methods for %s", username)
        graph_error = "Could not retrieve authentication methods at the moment."

    return render(
        request,
        "core/profile.html",
        {
            "cas_attributes": attributes,
            "resolved_upn": username,
            "auth_methods": auth_methods,
            "graph_error": graph_error,
        },
    )


@login_required
def reset_mfa(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    username = normalize_username(request.user.username)
    methods = []
    mfa_methods = []

    try:
        methods = list_user_authentication_methods(username)
        mfa_methods = prepare_auth_methods(methods)

        message = reset_mfa_methods(username, mfa_methods)
        log_mfa_reset_event(
            request=request,
            username=username,
            status="success",
            attempted_methods=mfa_methods,
            existing_methods=methods,
            result_message=message,
        )

        return JsonResponse(
            {
                "success": True,
                "message": message,
            },
            status=200,
        )

    except Exception as exc:
        logger.exception("Failed to reset MFA methods for %s", username)
        log_mfa_reset_event(
            request=request,
            username=username,
            status="failure",
            attempted_methods=mfa_methods,
            existing_methods=methods,
            failure_reason=str(exc),
        )
        return JsonResponse(
            {
                "success": False,
                "message": str(exc),
            },
            status=500,
        )


class MitIDLoginView(CASLoginView):
    def get(self, request, *args, **kwargs):
        ticket_present = bool(request.GET.get("ticket"))
        service_url = request.build_absolute_uri()

        try:
            response = super().get(request, *args, **kwargs)
        except PermissionDenied as exc:
            if ticket_present:
                log_mitid_login_failure(
                    request=request,
                    failure_reason=str(exc),
                    service_url=service_url,
                )
            raise

        if ticket_present and not request.user.is_authenticated:
            log_mitid_login_failure(
                request=request,
                failure_reason=(
                    f"CAS ticket validation failed with response status "
                    f"{response.status_code}"
                ),
                service_url=service_url,
            )

        return response
