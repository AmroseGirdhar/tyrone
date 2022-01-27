# Generated by Django 1.11.9 on 2018-02-20 22:06

from django.db import migrations, models
import django.db.models.deletion

import maasserver.models.node


class Migration(migrations.Migration):

    dependencies = [("maasserver", "0146_add_rootkey")]

    operations = [
        migrations.AddField(
            model_name="bmc",
            name="zone",
            field=models.ForeignKey(
                default=maasserver.models.node.get_default_zone,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="maasserver.Zone",
                verbose_name="Physical zone",
            ),
        )
    ]
