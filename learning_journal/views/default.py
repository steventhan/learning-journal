from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Journal


# @view_config(route_name='default', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(Journal)
#         journal = query.filter(Journal.title == 'Test').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'title': journal.title, 'project': 'learning_journal'}


@view_config(
    route_name='home', renderer='learning_journal:templates/home.html'
)
def home_view(request):
    """Render home.html at '/'"""
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        new_entry = Journal(title=title, body=body)
        request.dbsession.add(new_entry)
    try:
        journal_entries = request.dbsession.query(Journal).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {
        'title': 'Home',
        'journal_entries': journal_entries
    }


@view_config(
    route_name='new-entry',
    renderer='learning_journal:templates/new-entry.html'
)
def new_entry(request):
    """Render new-entry.html at '/new-entry'"""
    return {
        'title': 'New entry'
    }


@view_config(
    route_name='single-entry',
    renderer='learning_journal:templates/single-entry.html'
)
def single_entry(request):
    """Render single entry at '/journal/{id}'"""
    try:
        journal = request.dbsession.query(Journal).filter_by(
            id=request.matchdict['id']
        ).first()
    except:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {
        'title': 'Single entry',
        'journal': journal
    }


@view_config(
    route_name='edit-entry',
    renderer='learning_journal:templates/edit-entry.html'
)
def edit_entry(request):
    """Render edit-entry.html at '/journal/12345/edit-entry'"""
    return {
        'title': 'Edit entry'
    }


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
