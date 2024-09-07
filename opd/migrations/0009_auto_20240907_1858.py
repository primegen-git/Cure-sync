from django.db import migrations
from django.contrib.auth.models import Group


def create_doctor_group(apps, schema_editor):
    doctor_group, created = Group.objects.get_or_create(name="Doctor")


class Migration(migrations.Migration):
    dependencies = [
        ("opd", "0008_machinery_remove_doctor_email_remove_doctor_username_and_more"),
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.RunPython(create_doctor_group),
    ]
