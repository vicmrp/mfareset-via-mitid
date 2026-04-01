from django.dispatch import receiver

from core.utils.audit import log_mitid_login_success

try:
    from django_cas_ng.signals import cas_user_authenticated
except ImportError:  # pragma: no cover
    cas_user_authenticated = None


if cas_user_authenticated is not None:

    @receiver(cas_user_authenticated)
    def record_cas_login_success(
        sender,
        user,
        service,
        request,
        username,
        **kwargs,
    ) -> None:
        log_mitid_login_success(
            request=request,
            username=username or user.get_username(),
            service_url=service or "",
        )
