import random
import string
from functools import wraps
from random import choice
from uuid import uuid4

import mimesis
from django.db.models.fields.files import FieldFile


class ObfuscatorConfigError(Exception):
    pass


__country_code__ = 'DE'
__pers__ = mimesis.Person(__country_code__)
__addr__ = mimesis.Address(__country_code__)
__text__ = mimesis.Text(__country_code__)
__business__ = mimesis.Business(__country_code__)
__www = mimesis.Internet()

first_level_domains = (
    'testify', 'thingify', 'suxxify',
    'xxxify', 'someify', 'thereify',
    'pastarify', 'greatify', 'biglify',
    'trumpify', 'proxify', 'heredocsify',
    'no-place-like-127-0-0-1',
    'selfify', 'awaitify', 'entropify',
    'luckify', 'stuffify', 'returning-with-zero-considered-harmfulify',
)

second_level_domains = (
    'test', 'thing', 'suxx',
    'xxx', 'some', 'there',
    'pasta', 'great', 'bigly',
    'trump', 'sad', 'here',
    'no-place-like-127-0-0-1',
    'self', 'await', 'entropy',
    'lucky', 'stuff', 'returning-with-zero-considered-harmful',
)

alphanumeric_characters = string.ascii_uppercase \
    + string.ascii_lowercase \
    + string.digits


def generate_domain_list(prefix=''):
    return [  # nosec
        f"""{prefix}{choice(first_level_domains)}.{choice(
            second_level_domains)}{__www.top_level_domain()}"""
        for _ in range(10 ** 5)
    ]


domain_list = generate_domain_list()
email_domain_list = generate_domain_list(prefix='@')

OBFUSCATORS_REGISTRY = {}


def obfuscator(fn):
    """
    This decorator registers function in global registry and changes
    """
    function_name = fn.__name__

    if function_name in OBFUSCATORS_REGISTRY:
        raise ObfuscatorConfigError(
            f'Obfuscator {function_name} is defined twice'
        )

    @wraps(fn)
    def wrapper(val, **kwargs):
        if val:
            return fn(val, **kwargs)
        else:
            return val

    OBFUSCATORS_REGISTRY[function_name] = wrapper

    return wrapper


@obfuscator
def shuffle(val):
    """Shuffle characters of initial value"""
    char_list = list(val)
    random.shuffle(char_list)
    return ''.join(char_list)


@obfuscator
def mask(val):
    """Replace string with same length string of *"""
    return "*" * len(val)


@obfuscator
def known_hash(_):
    return "pbkdf2_sha256$36000$bWQ1A1rEn8Iu$39OfcSAUeOoKem1" \
           "C279LwoK9v4xvCgbp7SsCdict/XU="


@obfuscator
def uuid(_):
    return str(uuid4())


@obfuscator
def filepath(val):
    """Replaces filename in input value (filepath normally) with *'s"""
    if isinstance(val, FieldFile):
        val = val.name
    *head, tail = val.split('/')
    return '/'.join(
        [f'{seg}' for seg in head]
    ) + f'/{(len(tail) - 4) * "*"}{tail[-4:]}'


@obfuscator
def filename(val, name_length=8):
    """Replaces filename with *'s, preserving file extension"""
    characters = string.ascii_lowercase + string.digits
    extension = val.split('.')[-1]
    name = ''.join(  # nosec
        random.choice(characters) for _ in range(name_length)
    )
    return f'{name}.{extension}'


@obfuscator
def search_text(val):
    return (f'{full_name(val=val)} {street_name(val=val)} '
            f'{street_number(val=val)} {__business__.company()} '
            f'{city(val=val)} {postal_code(val=val)} {country(val=val)}')


@obfuscator
def title(_):
    """Random salutation (Hr., Fr.)"""
    return choice(  # nosec
        ["Hr.", "Fr."]
    ) + choice(  # nosec
        ["Dr.", "Prof.", "Maj.", "Sayan"]
    )


@obfuscator
def first_name(_):
    return __pers__.name()


@obfuscator
def last_name(_):
    return __pers__.last_name()


@obfuscator
def full_name(val):
    return f'{first_name(val=val)} {last_name(val=val)}'


@obfuscator
def username(_):
    return __pers__.username(template='UU.d')


@obfuscator
def email(_):
    return __pers__.email(domains=email_domain_list)


@obfuscator
def url(_):
    """Random root url, for example http://a-domain.com/"""
    return f'http://{random.choice(domain_list)}/'  # nosec


@obfuscator
def phone_number(_):
    return __pers__.telephone()


@obfuscator
def shipping_adress(_):
    return (
        f'{__addr__.street_name()},'
        f'{ __addr__.street_number()},'
        f'{ __addr__.postal_code()},'
        f'{__addr__.city()}'
    )


@obfuscator
def street_name(_):
    return __addr__.street_name()


@obfuscator
def street_number(_):
    return __addr__.street_number()


@obfuscator
def province(_):
    return __addr__.province()


@obfuscator
def postal_code(_):
    return __addr__.postal_code()


@obfuscator
def city(_):
    return __addr__.city()


@obfuscator
def state(_):
    return __addr__.state()


@obfuscator
def country(_):
    return __addr__.country()


@obfuscator
def sentence(_):
    return __text__.sentence()


@obfuscator
def word(_):
    return __text__.word()


@obfuscator
def paragraph(value):
    if value:
        return __text__.text(quantity=1)[:len(value)]
    else:
        return ''


@obfuscator
def ipv4(_):
    return __www.ip_v4()


@obfuscator
def vat_number(_):
    return __country_code__.upper() + number(_)


@obfuscator
def number(_):
    return ''.join([choice(string.digits) for _ in range(9)])  # nosec


@obfuscator
def voucher(val):
    return ''.join((
        choice(string.ascii_uppercase)  # nosec
        for _ in range(len(val or 6))))


@obfuscator
def password(val):
    return ''.join(
        (choice(alphanumeric_characters)  # nosec
         for _
         in range(len(val)))
    )


@obfuscator
def key(_):
    return ''.join(
        [choice(alphanumeric_characters)  # nosec
         for _
         in range(16)]
    )


@obfuscator
def empty(_):
    """Empty string"""
    return ''


@obfuscator
def json(d):
    """Initial JSON with null values"""
    return {k: None for k, v in d.items()}


@obfuscator
def empty_json(_):
    """'{}'"""
    return {}
