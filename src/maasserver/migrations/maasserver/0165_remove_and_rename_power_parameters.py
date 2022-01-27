# Generated by Django 1.11.11 on 2018-06-02 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("maasserver", "0164_copy_over_existing_power_parameters")]

    operations = [
        migrations.RemoveField(model_name="bmc", name="power_parameters"),
        migrations.RemoveField(
            model_name="node", name="instance_power_parameters"
        ),
        migrations.RenameField(
            model_name="bmc",
            old_name="new_power_parameters",
            new_name="power_parameters",
        ),
        migrations.RenameField(
            model_name="node",
            old_name="new_instance_power_parameters",
            new_name="instance_power_parameters",
        ),
    ]
