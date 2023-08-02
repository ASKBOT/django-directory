"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""

from directory import views
from django.urls import re_path

urlpatterns = (
    re_path(r'^(?P<path>.*)$', views.browse, name='directory_browse'),
)
