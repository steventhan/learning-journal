import pytest
from pyramid import testing
from learning_journal.models import Entry


def test_entry_model(new_session):
    assert len(new_session.query(Entry).all()) == 0
    test_entry = Entry(title='Test entry', body='test body')
    new_session.add(test_entry)
    new_session.flush()
    assert len(new_session.query(Entry).all()) == 1


def dummy_http_request(new_session):
    test_request = testing.DummyRequest()
    test_request.dbsession = new_session
    return test_request


def test_home_view(new_session):
    from learning_journal.views.default import home_view
    new_session.add(Entry(title='Pytest', body='<h1>This is a pytest</h1>'))
    new_session.flush()
    http_request = dummy_http_request(new_session)
    result = home_view(http_request)
    assert result['journal_entries'][-1].title == 'Pytest'
    assert 'This is a pytest' in result['journal_entries'][-1].body


def test_single_entry_view(new_session):
    from learning_journal.views.default import single_entry
    new_session.add(Entry(title='Pytest', body='<h1>This is a pytest</h1>'))
    new_session.flush()
    http_request = dummy_http_request(new_session)
    http_request.matchdict['id'] = 1
    result = single_entry(http_request)
    assert result['journal'].title == 'Pytest'


def test_new_entry_view():
    from learning_journal.views.default import new_entry
    request = testing.DummyRequest()
    info = new_entry(request)
    assert ('error' and 'body' and 'entry_title') in info


def test_edit_entry_view():
    from learning_journal.views.default import edit_entry
    request = testing.DummyRequest()
    info = edit_entry(request)


# def test_home(testapp):
#     response = testapp.get('/', status=200)
#     assert b"Steven Than's Mockup" in response.body


# def test_single_entry(testapp):
#     response = testapp.get('/journal/1', status=200)
#     assert b'<h2 class="text-center">Test</h2>'\
#         in response.body


# def test_new_entry_not_logged_in(testapp):
#     response = testapp.get('/new-entry', status='*')
#     assert response.status_code == 403


def test_edit_entry_fobidden_not_logged_in(testapp):
    response = testapp.get('/journal/12345/edit-entry', status='*')
    assert response.status_code == 403
