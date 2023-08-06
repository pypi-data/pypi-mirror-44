import json
import os

from django.conf import settings

filename = os.path.join(
    settings.BASE_DIR,
    'data-obfuscation-rules.json',
)


def schema_exists():
    return os.path.isfile(filename)


def load_schema() -> dict:
    with open(filename, 'r') as models_file:
        schema = json.load(models_file)
    # convert list of "table","fields" maps to table:fields map
    return {
        table_metadata['table']: table_metadata.get('fields')
        for table_metadata
        in schema
    }


def dump_schema(schema):
    with open(filename, 'w') as models_file:
        json.dump(schema, models_file, indent=2)
