from pyramid.view import notfound_view_config


@notfound_view_config(renderer='learning_journal:templates/404.html')
def notfound_view(request):
    request.response.status = 404
    return {}
