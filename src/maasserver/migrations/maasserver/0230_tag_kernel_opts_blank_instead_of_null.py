# Generated by Django 2.2.12 on 2021-03-05 10:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0229_drop_physicalblockdevice_storage_pool"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="kernel_opts",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
    ]
