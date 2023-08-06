import sys
import typing as t

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection, ProgrammingError
from django.db.transaction import atomic

from django_obfucat.obfuscators import OBFUSCATORS_REGISTRY
from django_obfucat.utils import load_schema


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-input', '--noinput',
            action='store_false',
            dest='interactive',
            default=False,
            help='Shall we skip the second thoughts and just '
                 'nondiscursively obfuscate the database?'
        )

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                cursor.execute('select 1 from obfucatable')
            except ProgrammingError:
                print(
                    'This DB can not be obfuscated, as it does not have '
                    'safeguard. Create table named "obfucatable" and re-run '
                    'this command if you know what you are doing'
                )
                sys.exit(1)

        if options['interactive']:
            input(  # nosec
                'You are about to destroy DB data, press Ctrl-C to stop or '
                'Enter to continue'
            )

        schema: t.Dict = load_schema()

        for table_name, fields in schema.items():
            app_label, model_name = table_name.split('.')
            model_class = apps.get_model(app_label, model_name)

            if fields is None:
                print(f'Truncating `{table_name}`')
                truncate_table(model_class)

            else:
                fields_with_obfuscators = get_fields_with_obfuscators(fields)

                # check if any field needs to be obfuscated
                if not fields_with_obfuscators:
                    print(
                        f'Skipping `{table_name}`: '
                        f'no field need obfuscation'
                    )
                    continue

                line_count: int = model_class.objects.all().count()
                print(
                    f'Obfuscating `{table_name}` ({line_count})'
                )

                current_row_number = 0
                percent = 0

                all_objects = model_class.objects.all().iterator()

                with atomic():
                    for instance in all_objects:
                        updated_values = {}

                        for field_name, obfuscator_name \
                                in fields_with_obfuscators.items():
                            updated_values[field_name] = obfuscate(
                                    instance,
                                    field_name,
                                    obfuscator_name,
                                )

                        model_class.objects.filter(pk=instance.pk)\
                            .update(**updated_values)

                        current_row_number, percent = print_progressbar(
                            current_row_number,
                            percent,
                            line_count,
                        )
                print()


def get_fields_with_obfuscators(fields) -> t.Dict[str, str]:
    return {
        name: obfuscator_name
        for name, obfuscator_name
        in fields.items()
        if obfuscator_name is not None
    }


def obfuscate_value_with(value: str, obfuscator_name: str) -> str:
    obfuscator_function = OBFUSCATORS_REGISTRY[obfuscator_name]
    return obfuscator_function(value)


def truncate_table(model_class) -> None:
    with atomic():
        model_class.objects.all().delete()


def print_progressbar(
        current_number: int,
        current_percent: int,
        total_number: int,
) -> t.Tuple[int, int]:
    new_percent = int(100 * (current_number / total_number))
    if new_percent != current_percent:
        current_percent = new_percent
        if not new_percent % 10:
            progress = new_percent
        else:
            progress = '.'
        print(progress, end='', flush=True)
    return current_number + 1, current_percent


def obfuscate(instance, field_name, obfuscator_name):
    field_value = getattr(instance, field_name)
    return obfuscate_value_with(field_value, obfuscator_name)
