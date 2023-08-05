#!/usr/bin/env python

import os
import re
import sys
import codecs

from setuptools import setup, find_packages


# When creating the sdist, make sure the django.mo file also exists:
if 'sdist' in sys.argv or 'develop' in sys.argv:
    os.chdir('taggit_anywhere')
    try:
        from django.core import management
        management.call_command('compilemessages', stdout=sys.stderr, verbosity=1)
    except ImportError:
        if 'sdist' in sys.argv:
            raise
    finally:
        os.chdir('..')


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name="django-taggit-anywhere",
    version=find_version('taggit_anywhere', '__init__.py'),
    license="MIT License",

    install_requires=[
    ],
    requires=[
        'Django (>=1.4)',
    ],

    description="django-taggit with easy",
    long_description=read('README.rst'),
    
    author='Basil Shubin',
    author_email='basil.shubin@gmail.com',

    url='https://github.com/bashu/django-taggit-anywhere',
    download_url='https://github.com/bashu/django-taggit-anywhere/zipball/master',
    
    packages=find_packages(exclude=('example*',)),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',        
    ],
)
