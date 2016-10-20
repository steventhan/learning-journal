import pytest
from pyramid import testing
from learning_journal.models import (
        Entry,
        get_engine,
        get_session_factory,
        get_tm_session
)
from learning_journal.models.meta import Base
import transaction


@pytest.fixture(scope="session")
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include(".models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


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
    from .views.default import home_view
    new_session.add(Entry(title='Pytest', body='<h1>This is a pytest</h1>'))
    new_session.flush()
    http_request = dummy_http_request(new_session)
    result = home_view(http_request)
    assert result['journal_entries'][-1].title == 'Pytest'


def test_single_entry_view(new_session):
    from .views.default import single_entry
    new_session.add(Entry(title='Pytest', body='<h1>This is a pytest</h1>'))
    new_session.flush()
    http_request = dummy_http_request(new_session)
    http_request.matchdict['id'] = 1
    result = single_entry(http_request)
    assert result['journal'].title == 'Pytest'


def test_new_entry_view():
    from .views.default import new_entry
    request = testing.DummyRequest()
    info = new_entry(request)
    assert info['title'] == 'New entry'


def test_edit_entry_view():
    from .views.default import edit_entry
    request = testing.DummyRequest()
    info = edit_entry(request)
    assert info['title'] == 'Edit entry'


def test_home(testapp):
    response = testapp.get('/', status=200)
    assert b"Steven Than's Mockup" in response.body


def test_single_entry(testapp):
    response = testapp.get('/journal/1', status=200)
    assert b'<h2 class="text-center">Test</h2>'\
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
