from django.core.management.base import BaseCommand

from django_obfucat.obfuscators import OBFUSCATORS_REGISTRY


class Command(BaseCommand):
    def handle(self, *args, **options):
        for obfuscator_name, obfuscator_function in sorted(OBFUSCATORS_REGISTRY.items()):
            docstring = obfuscator_function.__doc__ or ''
            if docstring:
                print(f'{obfuscator_name}: {docstring}')
            else:
                print(obfuscator_name)
