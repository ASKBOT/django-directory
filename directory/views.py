"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""
import os
from django.conf import settings
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.http import StreamingHttpResponse, Http404
from django.shortcuts import render

from django.utils.module_loading import import_string as import_module


#utils functions
def check_access(request):
    """Returns true if user has access to the directory"""
    access_mode = getattr(settings, 'DIRECTORY_ACCESS_MODE', 'public')

    if access_mode == 'public':
        return True

    if access_mode == 'use-perms':
        if request.user.is_anonymous:
            return False
        return request.user.has_perm('directory.read')

    if access_mode == 'custom':
        check_perm = settings.DIRECTORY_ACCESS_FUNCTION
        if isinstance(check_perm, str):
            check_perm = import_module(check_perm)
        elif not hasattr(check_perm, '__call__'):
            raise ImproperlyConfigured(
                'DIRECTORY_ACCESS_FUNCTION must either be a function or python path'
            )
        return check_perm(request)

    raise ImproperlyConfigured(
        "Invalid setting DIRECTORY_ACCESS_MODE: only values "
        "'public', 'use-perms', and 'custom' are allowed"
    )

def _get_abs_virtual_root():
    return _eventual_path(settings.DIRECTORY_DIRECTORY)

def _inside_virtual_root(eventual_path):
    virtual_root = _get_abs_virtual_root()
    return os.path.commonprefix([virtual_root, eventual_path]) == virtual_root

def _eventual_path(path):
    return os.path.abspath(os.path.realpath(path))

def get_names(directory):
    """Returns list of file names within directory"""
    contents = os.listdir(directory)
    files, directories = [], []
    for item in contents:
        candidate = os.path.join(directory, item)
        if os.path.isdir(candidate):
            directories.append(item)
        else:
            files.append(item)
    return files, directories

def read_file_chunkwise(file_obj):
    """Reads file in 32Kb chunks"""
    while True:
        data = file_obj.read(32768)
        if not data:
            break
        yield data

def _to_link_tuple(directory, basename):
    path = os.path.join(directory, basename)
    if _inside_virtual_root(_eventual_path(path)):
        link_target = os.path.relpath(path, start=_get_abs_virtual_root())
    else:
        link_target = None
    return basename, link_target

def _to_lower(text):
    return text.lower()

def _list_directory(request, directory):
    """default view - listing of the directory"""
    if check_access(request):
        files, directories = get_names(directory)

        if directory == _get_abs_virtual_root():
            directory_name = ''
        else:
            directory_name = os.path.basename(directory) + '/'

        file_links = [_to_link_tuple(directory, f) for f in sorted(files, key=_to_lower)]
        dir_links = [_to_link_tuple(directory, d) for d in sorted(directories, key=_to_lower)]
        data = {
            'directory_name': directory_name,
            'directory_files': file_links,
            'directory_directories': dir_links
        }
        template = getattr(settings, 'DIRECTORY_TEMPLATE', 'directory/list.html')
        return render(request, template, data)
    raise PermissionDenied()

def _download_file(request, file_path):
    """Allows authorized user to download a given file"""
    if check_access(request):
        response = StreamingHttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_path)
        file_obj = open(file_path, 'rb')
        response.streaming_content = read_file_chunkwise(file_obj)
        return response
    raise PermissionDenied()


def browse(request, path):
    """Directory list view"""
    eventual_path = _eventual_path(os.path.join(settings.DIRECTORY_DIRECTORY, path))

    if not _inside_virtual_root(eventual_path):
        # Someone is playing tricks with .. or %2e%2e or so
        raise Http404

    if os.path.isfile(eventual_path):
        return _download_file(request, eventual_path)

    return _list_directory(request, eventual_path)
