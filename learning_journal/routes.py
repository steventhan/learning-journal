def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('new-entry', '/new-entry')
    config.add_route('single-entry', '/entry/{id:\d+}')
    config.add_route('edit-entry', '/entry/{id:\d+}/edit-entry')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
