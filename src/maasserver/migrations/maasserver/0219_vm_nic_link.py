# Generated by Django 2.2.12 on 2020-10-19 14:23

from django.db import migrations, models
import django.db.models.deletion

import maasserver.fields
import maasserver.models.cleansave


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0218_images_maas_io_daily_to_stable"),
    ]

    operations = [
        migrations.CreateModel(
            name="VirtualMachineInterface",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("updated", models.DateTimeField(editable=False)),
                (
                    "mac_address",
                    maasserver.fields.MACAddressField(blank=True, null=True),
                ),
                (
                    "attachment_type",
                    models.CharField(
                        choices=[
                            ("network", "Network"),
                            ("bridge", "Bridge"),
                            ("macvlan", "Macvlan"),
                            ("sriov", "SR-IOV"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "host_interface",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="maasserver.Interface",
                    ),
                ),
                (
                    "vm",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interfaces_set",
                        to="maasserver.VirtualMachine",
                    ),
                ),
            ],
            options={
                "unique_together": {("vm", "mac_address")},
            },
            bases=(
                maasserver.models.cleansave.CleanSave,
                models.Model,
                object,
            ),
        ),
    ]
