def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('new-entry', '/new-entry')
    config.add_route('single-entry', '/journal/{id:\d+}')
    config.add_route('edit-entry', '/journal/{id:\d+}/edit-entry')