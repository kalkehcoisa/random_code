#-*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages

__author__ = 'Jayme Tosi Neto'

extra = {}
if sys.version_info >= (3,):
    pass

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, '../README.txt')).read()
CHANGES = open(os.path.join(here, '../CHANGES.txt')).read()

requires = [
    'colander',
    'deform',
    'dogpile.cache',
    'dogpile.core',
    'Flask',
    'flask-admin',
    'Flask-Babel',
    'Flask-Classy',
    'flask-login',
    'flask_mongoengine',
    'Flask-Script',
    'Flask-Session',
    'Jinja2',
    'mongoengine',
    'nose',
    'Unidecode',
    'MarkupSafe',
    'wtforms',
    'Werkzeug',
    'itsdangerous',
    #'wsgiref',
]

setup(
    name='mosca',
    version='0.1.2.1',
    description='mosca',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        #https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Framework :: Pyramid",
        'Development Status :: 1 - Planning',

        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        'Topic :: Software Development :: Libraries',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'],
    author='Jayme Tosi Neto;',
    author_email='kalkehcoisa@gmail.com;',
    url='',
    keywords='web wsgi bfg flask mysql',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='mosca',
    install_requires=requires,
    dependency_links=[
    ],
    entry_points="""\
    [paste.app_factory]
    main = mosca:main
    [console_scripts]
    initialize_db = mosca.scripts.initializedb:main
    run_dev = mosca.scripts.run_dev:main
    """,
)
