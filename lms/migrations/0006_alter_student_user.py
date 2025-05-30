# Generated by Django 4.2 on 2025-02-26 09:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0005_alter_student_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="student",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
