from pyramid.response import Response 
import os

HERE = os.path.dirname(__file__)


def home_page(request):
    imported_text = open(os.path.join(HERE + '/static/', 'index.html')).read()
    return Response(imported_text)


def view_entry(request):
    imported_text = open(os.path.join(HERE + '/static/', 'single-entry.html')).read()
    return Response(imported_text)


def new_entry(request):
    imported_text = open(os.path.join(HERE + '/static/', 'new-entry.html')).read()
    return Response(imported_text)


def edit_entry(request):
    imported_text = open(os.path.join(HERE + '/static/', 'edit-entry.html')).read()
    return Response(imported_text)


def includeme(config):
    config.add_view(home_page, route_name='home')
    config.add_view(view_entry, route_name='single-entry')
    config.add_view(new_entry, route_name='new-entry')
    config.add_view(edit_entry, route_name='edit-entry')
