from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ..models import Entry
from pyramid.security import NO_PERMISSION_REQUIRED


@view_config(
    route_name='home',
    renderer='learning_journal:templates/home.html',
    permission=NO_PERMISSION_REQUIRED
)
def home_view(request):
    """Render home.html at '/'"""
    journal_entries = request.dbsession.query(Entry).order_by(
            Entry.creation_date.desc()
    ).all()
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
    title = body = error = ''
    if request.method == 'POST':
        title = request.params.get('title', '')
        body = request.params.get('body', '')
        if not title or not body:
            error = 'Title and body are required'
        else:
            new_entry = Entry(title=title, body=body)
            request.dbsession.add(new_entry)
            return HTTPFound(location=request.route_url('home'))
    return {
        'title': 'New entry',
        'entry_title': title,
        'body': body,
        'error': error
    }


@view_config(
    route_name='single-entry',
    renderer='learning_journal:templates/single-entry.html'
)
def single_entry(request):
    """Render single entry at '/journal/{id}'"""
    journal = request.dbsession.query(Entry).filter_by(
        id=request.matchdict['id']
    ).first()
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
