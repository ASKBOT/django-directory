A simple app
for Django 3.2.8 and Python 3.9.2
that allows listing and downloading files from a given directory,
while controlling who can access the files.

Installation
============
`python manage.py migrate` is not required as there are no models.

Add to the `settings.py` file::

    INSTALLED_APPS += ['directory']

    DIRECTORY_DIRECTORY = '/path/to/dir'

That's the directory to be listed.

Add to the `urls.py` file the url entry, e.g.:

    ('files/', include('directory.urls')),

Dependencies
============
If setting `DIRECTORY_ACCESS_MODE` is set to `'use-perms'`, or (possibly) `'custom'`,
then this app will require `django.contrib.auth` installed in the project.

Configuration
=============

Setting `DIRECTORY_ACCESS_MODE`, can be one of: `'public'`, `'use-perms'`, `'custom'`,
value `'public'` is default.

* value `'public'` means that anyone can see the directory and download files.
* `'use-perms'` means that django permission `'directory_read'` from `django.contrib.auth` will be checked
* `'custom'` - means that function provided with `DIRECTORY_ACCESS_FUNCTION` will be called to check the permission

`DIRECTORY_ACCESS_FUNCTION` - a function or python path to the custom permission checking function e.g. `'myapp.perms.check_get_backups_perm'`.

The function should accept parameter `request` and return a Boolean value - access granted if `True`.

`DIRECTORY_TEMPLATE` - path to the template file for the directory listing. Default value
is `'directory/list.html'`
