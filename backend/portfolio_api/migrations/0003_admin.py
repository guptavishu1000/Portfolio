from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")
    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="admin",
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
            password=make_password("adminpassword"),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio_api", "0002_alter_contact_options_alter_education_options_and_more"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
