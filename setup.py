"""Copyright Askbot SpA, 2014"""
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
import sys

setup(
    name = "django-directory",
    version = "0.0.1",
    description = 'A Django application to list and download files from a directory',
    packages = find_packages(),
    author = 'Evgeny.Fadeev',
    author_email = 'evgeny.fadeev@gmail.com',
    license = 'MIT',
    keywords = 'django, list, download, files, directory',
    url = 'https://github.com/ASKBOT/django-directory',
    include_package_data = True,
    #install_requires = list(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    long_description = """Provides a directory listing and links to files, while controlling who has the access"""
)
