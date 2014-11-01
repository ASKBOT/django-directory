"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""

from django.conf.urls import url
from directory import views

urlpatterns = (
    url(r'^$', views.index, name='directory_index'),
    url(r'^list/$', views.list_directory, name='directory_list'),
    url(r'^download-file/(?P<file_name>.*)/$', views.download_file, name='directory_download_file')
)
