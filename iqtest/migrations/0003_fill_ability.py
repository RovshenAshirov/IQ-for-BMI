# Generated by Django 4.1 on 2023-05-19 15:43
import json

from django.conf import settings
from django.db import migrations


def forwards_func(apps, schema_editor):
    Ability = apps.get_model('iqtest', 'Ability')
    abilities = json.loads(
        (settings.BASE_DIR / 'iqtest' / 'migrations' / 'ability_data' / 'ability.json').read_text(
            encoding="utf-8"))
    objs = []
    for ability in abilities:
        objs.append(Ability(id=ability.get('id'), iq=ability.get('iq'), ability=ability.get('ability')))

    Ability.objects.bulk_create(objs)


def reverse_func(apps, schema_editor):
    Ability = apps.get_model('iqtest', 'Test')
    Ability.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('iqtest', '0002_fill_test'),
    ]

    operations = [migrations.RunPython(forwards_func, reverse_func)]
