import pytest
import json
from learning_journal.scripts import api_import
from learning_journal.models import Entry
from requests import Response
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

FAKE_API_RESPONSE = [
    {
     'created': '2016-08-23T07:45:07.414469',
     'id': 706,
     'markdown': "",
     'text': "",
     'title': 'Week 3 day 1'
    },
    {
     'created': '2016-08-21T07:45:07.414469',
     'id': 76,
     'markdown': "",
     'text': "",
     'title': 'W1'
    },
    {
     'created': '2016-08-23T07:45:07.414469',
     'id': 67,
     'markdown': "",
     'text': "",
     'title': 'Week 3 day 1'
    }
]


@patch(
    'requests.get',
    return_value=MagicMock(
        spec=Response,
        status_code=200,
        response=json.dumps(FAKE_API_RESPONSE),
        json=MagicMock(return_value=FAKE_API_RESPONSE)
    )
)
def test_get_data_200(req):
    """Test get_data returns FAKE_API_RESPONSE when status_code is 200."""
    data = api_import.get_data('http://exmaple.com', '/path/to/api', 'apikey')
    assert len(data) == 3
    assert ('create' and 'id' and 'markdown' and 'text' and 'title') in data[0]


@patch(
    'requests.get',
    return_value=MagicMock(
        spec=Response,
        status_code=500,
        response=json.dumps(FAKE_API_RESPONSE),
        json=MagicMock(return_value=FAKE_API_RESPONSE)
    )
)
def test_get_data_error(req):
    """Test get_data returns FAKE_API_RESPONSE when status_code is 200."""
    with pytest.raises(ValueError) as raised:
        api_import.get_data(
            'http://exmaple.com', '/path/to/api', 'apikey'
        )
    assert 'Can\'t get data, check your input' in str(raised)


def test_save_entries_to_db(new_session, setup_test_env):
    """Test save_entries_to_db."""
    initial_entry_count = new_session.query(Entry).count()
    api_import.save_entries_to_db(FAKE_API_RESPONSE)
    after_entry_count = new_session.query(Entry).count()
    new_session.flush()
    assert after_entry_count == initial_entry_count + 2
