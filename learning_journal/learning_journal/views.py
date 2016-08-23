from pyramid.view import view_config


@view_config(
    route_name='home', renderer='learning_journal:templates/home.html'
)
def home_view(request):
    return {}


@view_config(
    route_name='new-entry',
    renderer='learning_journal:templates/new-entry.html'
)
def new_entry(request):
    return {}


@view_config(
    route_name='single-entry',
    renderer='learning_journal:templates/single-entry.html'
)
def single_entry(request):
    return {}


@view_config(
    route_name='edit-entry',
    renderer='learning_journal:templates/edit-entry.html'
)
def edit_entry(request):
    return {}
