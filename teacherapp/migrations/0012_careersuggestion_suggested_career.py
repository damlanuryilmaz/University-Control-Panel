# Generated by Django 5.1 on 2024-09-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teacherapp", "0011_remove_careersuggestion_certificate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="careersuggestion",
            name="suggested_career",
            field=models.TextField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
