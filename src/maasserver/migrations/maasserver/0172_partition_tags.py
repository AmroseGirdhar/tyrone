# Generated by Django 1.11.11 on 2018-09-10 15:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0171_remove_pod_host")]

    operations = [
        migrations.AddField(
            model_name="partition",
            name="tags",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        )
    ]
