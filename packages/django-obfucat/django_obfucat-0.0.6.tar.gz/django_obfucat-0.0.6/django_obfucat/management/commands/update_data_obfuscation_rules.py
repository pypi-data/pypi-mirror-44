from django import apps
from django.core.management.base import BaseCommand
from django.db import models

from django_obfucat.utils import schema_exists, dump_schema, load_schema


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not schema_exists():
            print('Writing initial file')
            # initial schema has all fields with no obfuscator assigned
            # to fields
            dump_schema(get_current_initial_schema())
            return

        previous_schema = load_schema()

        current_schema = get_current_schema()

        for table_metadata in current_schema:
            model_name = table_metadata['table']
            # if table is set to be cleared in previous schema
            # (i.e. it has no 'fields' key), delete it from processing

            table_marked_as_excluded = model_name in previous_schema \
                                       and not previous_schema[model_name]

            if table_marked_as_excluded:
                del table_metadata['fields']
                print(f'Excluded `{model_name}` from further processing')
                continue

            fields = table_metadata['fields'].copy()
            for field in fields.values():
                field_name = field.name
                obfuscator = get_field_obfuscator(
                    previous_schema,
                    model_name,
                    field_name,
                )

                existing_obfuscator_not_defined = obfuscator == ''

                if existing_obfuscator_not_defined:
                    table_metadata['fields'][field_name] = get_default_obfuscator(field)
                else:
                    table_metadata['fields'][field_name] = obfuscator

        print('Writing updated file')
        dump_schema(current_schema)


def get_field_obfuscator(schema, model_name, field_name):
    try:
        return schema[model_name][field_name]
    except KeyError:
        print(
            f'`{field_name}` in `{model_name}` is missing an obfuscator'
        )
        return ''


def get_model_name(model):
    return f'{model._meta.app_label}.{model.__name__}'


def get_current_schema():
    models_list = apps.apps.get_models()
    current_schema = []
    for model in models_list:
        current_schema.append({
            'table': get_model_name(model),
            'fields': {field.name: field
                       for field in model._meta.fields}
        })
    return current_schema


def get_default_obfuscator(field):
    if isinstance(field, (models.CharField, models.TextField)):
        return ''
    else:
        return None


def get_current_initial_schema():
    models_list = apps.apps.get_models()
    current_schema = []
    for model in models_list:
        current_schema.append({
            'table': get_model_name(model),
            'fields': {field.name: get_default_obfuscator(field)
                       for field
                       in model._meta.fields}
        })
    return current_schema
