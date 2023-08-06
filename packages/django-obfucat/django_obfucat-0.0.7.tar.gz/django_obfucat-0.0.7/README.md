# django_obfucat

Django ORM driven database obfuscation is making GDPR great again!

`django_obfucat` is useful when your developers need production database dump to 
experiment with it locally, and test fixtures or sample dump are too synthetic for that.
But production data contains private data, that you must not disclose or share.
Data obfuscation may help in this case. Data, being anonymized, while still having 
real-looking shape, is exactly what developers need for testing.

With `django_obfucat` you can quickly replace names, addresses and other deanonymizing
info with fake data, and do it multiple times, or automatically.

## installation

```bash
$ pip install django_obfucat
```
Add `'django_obfucat'` to `INSTALLED_APPS`

## workflow

### as developer

1. Run `./manage.py update_data_obfuscation_rules` after modifying any of 
your model classes. This will create (and update) file `data-obfuscation-rules.json`
in your Django project root.

2. Run `./manage.py validate_data_obfuscation_rules` and be informed of any 
fields that might need an obfuscator

3. Decide if those fields need obfuscators. For full list of available obfuscators,
run `./manage.py list_obfuscators`

4. Edit `data-obfuscation-rules.json` and replace values equal `""` with the 
appropriate obfuscator name

5. Commit `data-obfuscation-rules.json` with everything else


### as devops

0. Make sure you have backup of your DB

1. Create empty table `obfucatable` in target database:
`create table obfucatable (id int);`

2. Run `./manage.py obfuscate_data`

3. Make DB dump for your developers

### as obfuscator

It might not be necessary to add sophisticated obfuscators. You probably want
to reuse an existing obfuscator or just use "mask" or "empty".

Add a function with one argument (original value) like this in your code:

```python
from django_obfucat.obfuscators import obfuscator

@obfuscator
def arbitrary_field(v):  # 
    """This docstring will be shown by ./manage.py list_obfuscators"""
    return 'XXX'
```

Next, your obfuscator will be added in registry use the function's name, 
i.e. `arbitrary_field` as obfuscator in data-obfuscation-rules.json.

## data-obfuscation-rules.json

Default path is `BASE_DIR/data-obfuscation-rules.json`, can be overridden in `settings.py`:

```python
OBFUSCATION_RULES_FILE_PATH = os.path.join(BASE_DIR, 'settings/data-obfuscation-rules.json')
```

This pretty-formatted JSON file contains list of dicts. Each dict has at 
least one key `table`, which is django app-name.ModelName. Second key `fields` 
is another dict with keys - model field names, values - obfuscator name or null 
(for no action on that field).  

By default, only CharField and TextField and their inheritors will be subject to
obfuscation. This means, other fields will have `null` as obfuscator, and will not
be touched. If you need to obfuscate other field types, create obfuscator,
that returns that value type.

Example:
```
...
  {
    "table": "auth.Permission",
    "fields": {
      "id": null,
      "name": "shuffle",
      "content_type": null,
      "codename": null
    }
  },
...
```
Here, we use `shuffle` obfuscator for table of model class `Permission` from
`django.contrib.auth`. Other fields will keep their values. 

This might seem obvious, but DON'T obfuscate primary key fields. Also, better not 
obfuscate ForeignKey fields.

Tables, that must be fully cleaned by obfuscator, do not have `fields` key. Note,
table is flushed with `DELETE FROM <table_name>`. Any related foreign keyed relations
with `ON_DELETE=CASCADE` will be deleted automatically. On the other hand, 
relations with `ON_DELETE=PROTECT` will crash obfuscation.

## known limitations

* If your models have custom default managers with custom `get_queryset()`, that does 
not return all objects, respectively not all records will be obfuscated.
