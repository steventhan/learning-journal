import pytest
from pyramid import testing


def test_home_view():
    from .views import home_view
    request = testing.DummyRequest()
    info = home_view(request)
    assert info['title'] == 'Home'


def test_single_entry_view():
    from .views import single_entry
    request = testing.DummyRequest()
    info = single_entry(request)
    assert info['title'] == 'Single entry'


def test_new_entry_view():
    from .views import new_entry
    request = testing.DummyRequest()
    info = new_entry(request)
    assert info['title'] == 'New entry'


def test_edit_entry_view():
    from .views import edit_entry
    request = testing.DummyRequest()
    info = edit_entry(request)
    assert info['title'] == 'Edit entry'


def test_home(testapp):
    response = testapp.get('/', status=200)
    assert b"Steven Than's Mockup" in response.body


def test_single_entry(testapp):
    response = testapp.get('/journal/12345', status=200)
    assert b'<h2 class="text-center">This is a blog title</h2>'\
        in response.body


def test_new_entry(testapp):
    response = testapp.get('/new-entry', status=200)
    assert b"<title>Steven's Learning Journal | New entry</title>"\
        in response.body


def test_edit_entry(testapp):
    response = testapp.get('/journal/12345/edit-entry', status=200)
    assert b'<input type="email" class="form-control" id="title" ' +\
        b'placeholder="Journal title" value="This is a blog title">'\
        in response.body
