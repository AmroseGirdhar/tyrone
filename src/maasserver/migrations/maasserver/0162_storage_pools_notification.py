# Generated by Django 1.11.11 on 2018-04-04 09:38

import datetime

from django.db import migrations

from maasserver.enum import BMC_TYPE


def forwards(apps, schema_editor):
    BMC = apps.get_model("maasserver", "BMC")
    Notification = apps.get_model("maasserver", "Notification")
    for pod in BMC.objects.filter(bmc_type=BMC_TYPE.POD, power_type="virsh"):
        now = datetime.datetime.utcnow()
        Notification.objects.create(
            admins=True,
            message=(
                "Pod %s needs to be refreshed to gather storage pool "
                "information." % pod.name
            ),
            created=now,
            updated=now,
        )


def backwards(apps, schema_editor):
    # No reason just can't go backwards, but keep the notifications.
    pass


class Migration(migrations.Migration):

    dependencies = [("maasserver", "0161_pod_storage_pools")]

    operations = [migrations.RunPython(forwards, backwards)]
