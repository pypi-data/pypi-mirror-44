import sys

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models

from django_obfucat.obfuscators import OBFUSCATORS_REGISTRY
from django_obfucat.utils import load_schema


class Command(BaseCommand):
    def handle(self, *args, **options):
        schema = load_schema()
        exit_code = 0
        for table_name, fields in schema.items():
            app_label, model_name = table_name.split('.')

            try:
                model_class = apps.get_model(app_label, model_name)
            except LookupError:
                print(
                    f'`{table_name}` model not found in apps'
                )
                exit_code = 1
            else:
                if not issubclass(model_class, models.Model):
                    print(
                        f'`{table_name}` is not valid Model class name'
                    )
                    exit_code = 1

            if fields:
                for field_name, obfuscator_name in fields.items():
                    if obfuscator_name == '':
                        print(
                            f'`{table_name}.{field_name}` does not have '
                            f'obfuscator assigned, give it obfuscator name or '
                            f'use "null" to not obfuscate it'
                        )
                        exit_code = 1

                    if obfuscator_name \
                            and obfuscator_name not in OBFUSCATORS_REGISTRY:
                        print(
                            f'`{table_name}.{field_name}` has unknown '
                            f'obfuscator: {obfuscator_name}'
                        )
                        exit_code = 2

        sys.exit(exit_code)
