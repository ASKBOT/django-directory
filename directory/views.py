"""Copyright Askbot SpA 2014, Licensed under GPLv3 license."""
import os
from django.conf import settings
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import StreamingHttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

try:
    from django.utils.module_loading import import_string as import_module
except ImportError:
    from django.utils.module_loading import import_by_path as import_module

#utils functions
def check_access(request):
    """Returns true if user has access to the directory"""
    access_mode = getattr(settings, 'DIRECTORY_ACCESS_MODE', 'public')
    if access_mode == 'public':
        return True
    elif access_mode == 'use-perms':
        if request.user.is_anonymous():
            return False
        else:
            return request.user.has_perm('directory.read')
    elif access_mode == 'custom':
        check_perm = settings.DIRECTORY_ACCESS_FUNCTION
        if isinstance(check_perm, basestring):
            check_perm = import_module(check_perm)
        elif not hasattr(check_perm, '__call__'):
            raise ImproperlyConfigured('DIRECTORY_ACCESS_FUNCTION must either be a function or python path')
        return check_perm(request)
    else:
        raise ImproperlyConfigured(
            "Invalid setting DIRECTORY_ACCESS_MODE: only values "
            "'public', 'use-perms', and 'custom' are allowed"
        )


def get_file_names(directory):
    """Returns list of file names within directory"""
    contents = os.listdir(directory)
    files = list()
    for item in contents:
        if os.path.isfile(os.path.join(directory, item)):
            files.append(item)
    return files

def read_file_chunkwise(file_obj):
    """Reads file in 32Kb chunks"""
    while True:
        data = file_obj.read(32768)
        if not data:
            break
        yield data

#view functions below
def index(request):
    return HttpResponseRedirect(reverse('directory_list'))

def list_directory(request):
    """default view - listing of the directory"""
    if check_access(request):
        directory = settings.DIRECTORY_DIRECTORY
        data = {
            'directory_name': os.path.basename(directory),
            'directory_files': get_file_names(directory)
        }
        template = getattr(settings, 'DIRECTORY_TEMPLATE', 'directory/list.html')
        return render(request, template, data)
        
    else:
        raise PermissionDenied()

def download_file(request, file_name):
    """allows authorized user to download a given file"""

    if os.path.sep in file_name:
        raise PermissionDenied()

    if check_access(request):
        directory = settings.DIRECTORY_DIRECTORY

        #make sure that file exists within current directory
        files = get_file_names(directory)
        if file_name in files:
            file_path = os.path.join(directory, file_name)
            response = StreamingHttpResponse(mimetype='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            file_obj = open(os.path.join(directory, file_name))
            response.streaming_content = read_file_chunkwise(file_obj)
            return response
        else:
            raise Http404
