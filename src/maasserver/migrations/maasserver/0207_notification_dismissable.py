# Generated by Django 1.11.11 on 2020-05-05 13:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0206_remove_node_token")]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="dismissable",
            field=models.BooleanField(default=True),
        )
    ]
