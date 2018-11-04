#! /usr/bin/env bash
# Copyright Sebastian Pipping, Licensed under GPLv3 license.
set -e
set -u

: ${PYTHON:=python3}
: ${VIRTUALENV_NAME:=py3}
: ${DIRECTORY:=.}

if [[ -z $(type -P "${PYTHON}") ]]; then
    echo "ERROR: A python version 3 executable is expected to be on your path" >&2
    echo "edit the path above or install python 3 and try again." >&2
    exit 1
fi

virtualenv --python=${PYTHON} ${VIRTUALENV_NAME}
set +u; source ${VIRTUALENV_NAME:?}/bin/activate; set -u

./setup.py develop

if [[ ! -d demo ]]; then
    django-admin startproject demo
    echo $'from django.urls import include, path\nurlpatterns.append(path("files/", include("directory.urls")))' >> demo/demo/urls.py
    echo "DIRECTORY_DIRECTORY = '${DIRECTORY}'"$'\n'"INSTALLED_APPS += ['directory']" >> demo/demo/settings.py
fi

python demo/manage.py runserver
