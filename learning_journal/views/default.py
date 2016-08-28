from pyramid.view import view_config

from ..models import Entry


@view_config(
    route_name='home', renderer='learning_journal:templates/home.html'
)
def home_view(request):
    """Render home.html at '/'"""
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        new_entry = Entry(title=title, body=body)
        request.dbsession.add(new_entry)
    journal_entries = request.dbsession.query(Entry).all()
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
