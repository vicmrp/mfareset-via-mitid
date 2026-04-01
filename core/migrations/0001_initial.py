from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MitIDLoginEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("username", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(choices=[("success", "Success"), ("failure", "Failure")], max_length=16)),
                ("service_url", models.TextField(blank=True)),
                ("failure_reason", models.TextField(blank=True)),
                ("ticket_present", models.BooleanField(default=False)),
                ("session_key", models.CharField(blank=True, max_length=255)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="MFAResetEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("username", models.CharField(max_length=255)),
                ("status", models.CharField(choices=[("success", "Success"), ("failure", "Failure")], max_length=16)),
                ("attempted_methods", models.JSONField(blank=True, default=list)),
                ("existing_methods", models.JSONField(blank=True, default=list)),
                ("result_message", models.TextField(blank=True)),
                ("failure_reason", models.TextField(blank=True)),
                ("session_key", models.CharField(blank=True, max_length=255)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
