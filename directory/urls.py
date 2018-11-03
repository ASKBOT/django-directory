"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""

from django.conf.urls import url
from directory import views

urlpatterns = (
    url(r'^(?P<path>.*)$', views.browse, name='directory_browse'),
)
