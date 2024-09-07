from django.db import migrations
from django.contrib.auth.models import Group


def create_profile_group(apps, schema_editor):
    profile_group, created = Group.objects.get_or_create(name="Profile")


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_alter_profile_name_alter_profile_username"),
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.RunPython(create_profile_group),
    ]
