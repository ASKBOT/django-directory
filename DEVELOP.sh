#! /usr/bin/env bash
# Copyright Sebastian Pipping, Licensed under GPLv3 license.

set -e
set -u

virtualenv_name=py27
virtualenv --python=python2 ${virtualenv_name}
set +u; source ${virtualenv_name:?}/bin/activate; set -u

./setup.py develop

if [[ ! -d demo ]]; then
    django-admin startproject demo
    echo $'from django.conf.urls import include\nurlpatterns.append(url("^files/", include("directory.urls")))' >> demo/demo/urls.py
    echo $'DIRECTORY_DIRECTORY = "."\nINSTALLED_APPS += ["directory"]' >> demo/demo/settings.py
fi

python2 demo/manage.py runserver
