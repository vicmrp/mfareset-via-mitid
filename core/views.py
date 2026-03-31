from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.utils.graph import list_user_authentication_methods
from core.utils.auth_methods import prepare_auth_methods
import logging


import time
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "core/home.html")


@login_required
def profile(request):
    attributes = request.session.get("attributes", {})
    auth_methods = []
    graph_error = None

    try:
        username = request.user.username.strip().lower()
        if "@" not in username:
            username = f"{username}@dtu.dk"

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
    # Real mfa reset method remains to be implemented

    #### dummy response #####
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    time.sleep(5)  # simulate long-running reset

    return JsonResponse({
        "success": True,
        "message": "MFA reset completed."
    }, status=200)
    #### dummy response #####