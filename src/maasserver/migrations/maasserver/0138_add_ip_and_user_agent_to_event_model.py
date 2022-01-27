# Generated by Django 1.11.6 on 2018-01-06 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("maasserver", "0137_create_default_roles")]

    operations = [
        migrations.AddField(
            model_name="event",
            name="ip_address",
            field=models.GenericIPAddressField(
                blank=True, default=None, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="user_agent",
            field=models.CharField(blank=True, default="", max_length=32),
        ),
    ]
