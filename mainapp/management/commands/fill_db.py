"""
Скрипт для добавления данных в БД проекта
"""
import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--data', required=True, type=str,
            help='name of json data file, placed in media/data'
        )

    def handle(self, *args, **options):
        inp_data = os.path.join(settings.MEDIA_ROOT, 'data', options['data'])
        with open(inp_data, 'r', encoding='utf-8') as data_file:
            try:
                inp_data = json.load(data_file)
                init_data = inp_data['init']
                object_list = inp_data['objects']
            except KeyError:
                print('data file structure is incorrect')
                return
        model = apps.get_model(init_data['app_label'], init_data['model_name'])
        rel_models = []
        for related in init_data['related']:
            rel_model = {'field': related['field']}
            rel_model['model'] = apps.get_model(related['app_label'], related['model_name'])
            rel_model['key'] = related['key']
            rel_models.append(rel_model)
        for obj in object_list:
            for related in rel_models:
                try:
                    inp_data = {related['key']: obj[related['field']]}
                    obj[related['field']] = related['model'].objects.get(**inp_data)
                except related['model'].DoesNotExist:
                    print('{} с параметром {} равным {} не найден'.format(
                        related['model'].__class__.__name__,
                        related['key'],
                        obj[related['field']]
                    ))
                    return
            new_obj, inp_data = model.objects.get_or_create(**obj)
            if inp_data:
                new_obj.save()
                