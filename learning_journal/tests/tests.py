import pytest
from pyramid import testing
from learning_journal.models import Entry


def test_entry_model(new_session):
    assert len(new_session.query(Entry).all()) == 0
    test_entry = Entry(title='Test entry', body='test body')
    new_session.add(test_entry)
    new_session.flush()
    assert len(new_session.query(Entry).all()) == 1


def test_home_view(new_session, dummy_http_request):
    from learning_journal.views.default import home_view
    new_session.add(Entry(title='Pytest', body='<h1>This is a pytest</h1>'))
    new_session.flush()
    result = home_view(dummy_http_request)
    assert result['journal_entries'][-1].title == 'Pytest'
    assert 'This is a pytest' in result['journal_entries'][-1].body


def test_single_entry_view(new_session, dummy_http_request):
    from learning_journal.views.default import single_entry
    new_session.add(Entry(title='Pytest', body='<h1>This is a pytest</h1>'))
    new_session.flush()
    dummy_http_request.matchdict['id'] = 1
    result = single_entry(dummy_http_request)
    assert result['entry'].title == 'Pytest'


def test_new_entry_view():
    from learning_journal.views.default import new_entry
    request = testing.DummyRequest()
    info = new_entry(request)
    assert ('error' and 'body' and 'entry_title') in info


def test_edit_entry_view(new_session, dummy_http_request):
    from learning_journal.views.default import edit_entry
    new_session.add(Entry(title='Pytest', body='<h1>This is a pytest</h1>'))
    new_session.flush()
    dummy_http_request.matchdict['id'] = 1
    response = edit_entry(dummy_http_request)
    assert response['entry'].title == 'Pytest'
    assert 'This is a pytest' in response['entry'].body


def test_new_entry_not_logged_in(testapp):
    response = testapp.get('/new-entry', status='*')
    assert response.status_code == 403


def test_edit_entry_fobidden_not_logged_in(testapp):
    response = testapp.get('/entry/12345/edit-entry', status='*')
    assert response.status_code == 403
