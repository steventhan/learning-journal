from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models import Entry
from ..security import check_credentials


@view_config(
    route_name='home',
    renderer='learning_journal:templates/home.html',
)
def home_view(request):
    """Render home.html at '/'"""
    journal_entries = request.dbsession.query(Entry).order_by(
            Entry.creation_date.desc()
    ).all()
    return {
        'journal_entries': journal_entries
    }


@view_config(
    route_name='new-entry',
    renderer='learning_journal:templates/new-entry.html',
    permission='modify'
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
        'entry_title': title,
        'body': body,
        'error': error
    }


@view_config(
    route_name='single-entry',
    renderer='learning_journal:templates/single-entry.html'
)
def single_entry(request):
    """Render single entry at '/entry/{id}'"""
    entry = request.dbsession.query(Entry).filter_by(
        id=request.matchdict['id']
    ).first()
    return {
        'entry': entry
    }


@view_config(
    route_name='edit-entry',
    renderer='learning_journal:templates/edit-entry.html',
    permission='modify'
)
def edit_entry(request):
    """Render edit-entry.html.'"""
    entry = request.dbsession.query(Entry).filter_by(
        id=request.matchdict['id']
    ).first()
    error = ''
    if request.method == 'POST':
        title = request.params.get('title', '')
        body = request.params.get('body', '')
        if not title or not body:
            error = 'Title and body are required'
        else:
            entry.title = title
            entry.body = body
            return HTTPFound(location=request.route_url('home'))
    return {
        'entry': entry,
        'error': error,
    }


@view_config(
    route_name='login',
    renderer='../templates/login.html'
)
def login(request):
    error = ''
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(
                location=request.route_url('home'),
                headers=headers
            )
        else:
            error = 'Unsuccessful, try again'
    return {'error': error}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
