# -*- coding: utf8 -*-
import pathlib

from setuptools import setup

from django_obfucat import VERSION

with open(pathlib.Path(__file__).parent / 'README.md') as readme:
    README = readme.read()

setup(
    name='django_obfucat',
    version=VERSION,
    packages=['django_obfucat'],
    include_package_data=True,
    license='MIT License',
    description='Data obfuscation tool for GDPR-compliant development process',
    long_description=README,
    url='https://bitbucket.org/3yourmind/django-obfucat',
    author='Serhii Zavadskyi',
    author_email='sz@3yourmind.com',
    install_requires=['mimesis'],
    classifiers=[
        'Environment :: Web Environment',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database',
        'Topic :: Utilities',
    ],
    keywords='',
)
