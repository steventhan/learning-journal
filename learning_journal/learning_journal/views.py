from pyramid.view import view_config


@view_config(
    route_name='home', renderer='learning_journal:templates/home.html'
)
def home_view(request):
    """Render home.html at '/'"""
    return {}


@view_config(
    route_name='new-entry',
    renderer='learning_journal:templates/new-entry.html'
)
def new_entry(request):
    """Render new-entry.html at '/new-entry'"""
    return {}


@view_config(
    route_name='single-entry',
    renderer='learning_journal:templates/single-entry.html'
)
def single_entry(request):
    """Render single-entry.html at '/journal/12345'"""
    return {}


@view_config(
    route_name='edit-entry',
    renderer='learning_journal:templates/edit-entry.html'
)
def edit_entry(request):
    """Render edit-entry.html at '/journal/12345/edit-entry'"""
    return {}
