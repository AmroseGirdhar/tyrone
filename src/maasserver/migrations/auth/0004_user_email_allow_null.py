# Generated by Django 1.11.9 on 2018-02-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("auth", "0003_django_1_11_update")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254,
                null=True,
                unique=True,
                verbose_name="email address",
            ),
        )
    ]
