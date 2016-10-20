import pytest
from pyramid import testing
import os
from learning_journal.models import (
        Entry,
        get_engine,
        get_session_factory,
        get_tm_session
)
from learning_journal.models.meta import Base
import transaction

DB_SETTINGS = {
    'sqlalchemy.url': 'postgres://steven:@localhost:5432/learning_journal_test'
}


@pytest.fixture(scope='function')
def setup_test_env():
    os.environ['DATABASE_URL'] = DB_SETTINGS['sqlalchemy.url']


@pytest.fixture(scope='function')
def sqlengine(request):
    config = testing.setUp(settings=DB_SETTINGS)
    config.include("learning_journal.models")
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


@pytest.fixture()
def testapp():
    from learning_journal import main
    app = main({})
    from webtest import TestApp
    return TestApp(app)
