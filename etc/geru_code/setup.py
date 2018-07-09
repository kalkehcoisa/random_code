import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import shlex
import sys

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name='geru',
    version='0.0',
    description='geru',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=[
        'pytest==3.6.1',
        'pytest-cov==2.5.1',
        'httpretty==0.9.4'
    ],
    install_requires=[
        'dogpile.cache==0.6.5',
        'plaster-pastedeploy==0.5',
        'pyramid==1.9.2',
        'pyramid-debugtoolbar==4.4',
        'pyramid-jinja2==2.7',
        'pyramid-nacl-session==0.3',
        'pyramid-restful-framework==1.0.0',
        'pyramid-retry==0.5',
        'pyramid-tm==2.2',
        'requests==2.18.4',
        'SQLAlchemy==1.2.8',
        'transaction==2.2.1',
        'zope.sqlalchemy==1.0',
        'waitress==1.1.0',
    ],
    entry_points={
        'paste.app_factory': [
            'main = geru:main',
        ],
        'console_scripts': [
            'initialize_geru_db = geru.scripts.initializedb:main',
        ],
    },
)
