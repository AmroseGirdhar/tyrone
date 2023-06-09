# Generated by Django 2.2.12 on 2022-01-12 09:47

from django.db import migrations
from django.db.models import Count
from django.utils import timezone


def create_default_nodeconfig_devices(apps, schema_editor):
    Node = apps.get_model("maasserver", "Node")
    NodeConfig = apps.get_model("maasserver", "NodeConfig")
    now = timezone.now()

    # find IDs for devices without node configs, create default one
    device_ids = (
        Node.objects.annotate(configs_count=Count("nodeconfig"))
        .filter(configs_count=0)
        .values_list("id", flat=True)
    )
    NodeConfig.objects.bulk_create(
        [
            NodeConfig(node_id=device_id, created=now, updated=now)
            for device_id in device_ids
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0253_nodeconfig"),
    ]

    operations = [
        migrations.RunPython(create_default_nodeconfig_devices),
    ]
