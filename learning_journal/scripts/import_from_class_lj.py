import requests
import os
from ..models import Entry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_data(domain, path, api_key=None):
    """Put together a GET request. Return json data"""
    params = {'apikey': api_key}
    res = requests.get(domain + path, params=params)
    if res.status_code == 200:
        return res.json()
    raise ValueError('Can\'t get data, check your input')


def save_entries_to_db(entries):
    """Save entries received from API to PostGres."""
    engine = create_engine(os.environ['DATABASE_URL'])
    Session = sessionmaker(bind=engine)
    session = Session()
    for entry in entries:
        if session.query(Entry).filter_by(title=entry['title']).count() == 0:
            session.add(Entry(
                title=entry['title'],
                body=entry['markdown'],
                creation_date=entry['created']
            ))
            session.commit()


def main():
    domain = 'https://sea401d4.crisewing.com'
    path = '/api/export'
    api_key = os.environ['API_KEY']
    save_entries_to_db(get_data(domain, path, api_key))
