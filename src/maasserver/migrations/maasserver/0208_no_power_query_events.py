# Generated by Django 1.11.11 on 2020-01-14 21:55

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import migrations
from django.db.models import Count


def delete_power_query_events(apps, schema_editor):
    Event = apps.get_model("maasserver", "Event")
    EventType = apps.get_model("maasserver", "EventType")
    power_query_event_types = EventType.objects.filter(
        name__in=["NODE_POWER_QUERIED_DEBUG", "NODE_POWER_QUERIED"]
    )
    power_query_events = Event.objects.filter(type__in=power_query_event_types)
    power_query_events.delete()
    power_query_event_types.delete()


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0207_notification_dismissable")]

    operations = [migrations.RunPython(delete_power_query_events)]
