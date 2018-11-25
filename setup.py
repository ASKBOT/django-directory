#! /usr/bin/env python
"""Copyright Askbot, SpA"""
from setuptools import setup, find_packages

setup(
    name='django-directory',
    version = '0.0.3',
    description = 'A Django application to list and download files from a directory',
    packages = find_packages(),
    author = 'Evgeny.Fadeev',
    author_email = 'evgeny.fadeev@gmail.com',
    license = 'GPLv3',
    keywords = 'django, list, download, files, directory',
    url = 'https://github.com/ASKBOT/django-directory',
    include_package_data = True,
    install_requires = [
        'Django >=1.11.16',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    long_description = """Provides a directory listing and links to files, while controlling who has the access"""
)
