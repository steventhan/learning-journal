from pyramid.response import Response
from pyramid.view import view_config
import os

HERE = os.path.dirname(__file__)


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_page(request):
    return []


@view_config(route_name='detail', renderer='templates/home.jinja2')
def detail_view(request):
    return {"content": "This was transformed into an HTTP response"}


def view_entry(request):
    imported_text = open(os.path.join(HERE + '/static/', 'single-entry.html')).read()
    return Response(imported_text)


def new_entry(request):
    imported_text = open(os.path.join(HERE + '/static/', 'new-entry.html')).read()
    return Response(imported_text)


def edit_entry(request):
    imported_text = open(os.path.join(HERE + '/static/', 'edit-entry.html')).read()
    return Response(imported_text)
