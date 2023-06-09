# Generated by Django 2.2.12 on 2021-02-22 11:23

from django.db import migrations


def drop_rsd_pods(apps, schema_editor):
    Pod = apps.get_model("maasserver", "Pod")
    Pod.objects.filter(power_type="rsd").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0224_virtual_machine_disk"),
    ]

    operations = [
        migrations.RunPython(drop_rsd_pods),
    ]
