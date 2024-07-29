import sqlite3

from app import app
from flask import g
import hmac
import hashlib


def get_db_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def generate_vacancy_token(company_login, vacancy_id):
    message = f'{company_login}:{vacancy_id}'.encode('utf-8')
    return hmac.new(app.config['SECRET_KEY'].encode('utf-8'), message, hashlib.sha256).hexdigest()
