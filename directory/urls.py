"""Copyright Askbot SpA 2023, Licensed under GPLv3 license."""
from django.urls import re_path

from directory import views

urlpatterns = (
    re_path(r'^(?P<path>.*)$', views.browse, name='directory_browse'),
)
