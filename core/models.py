from django.db import models


class MitIDLoginEvent(models.Model):
    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failure"
    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILURE, "Failure"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    service_url = models.TextField(blank=True)
    failure_reason = models.TextField(blank=True)
    ticket_present = models.BooleanField(default=False)
    session_key = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        username = self.username or "unknown-user"
        return f"{self.status} login for {username} at {self.created_at.isoformat()}"


class MFAResetEvent(models.Model):
    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failure"
    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILURE, "Failure"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    attempted_methods = models.JSONField(default=list, blank=True)
    existing_methods = models.JSONField(default=list, blank=True)
    result_message = models.TextField(blank=True)
    failure_reason = models.TextField(blank=True)
    session_key = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.status} MFA reset for {self.username} at {self.created_at.isoformat()}"
