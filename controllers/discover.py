from app import app
from flask import url_for, request, render_template, redirect, session, abort
from models.company_profile_model import get_vacancy, get_vacancy_by_token
from utils import get_db_connection, generate_vacancy_token


@app.route('/searching/<query>')
def index(query):
    conn = get_db_connection()
    vacancy = get_vacancy_by_token(conn, query)
    if vacancy:
        expected_token = generate_vacancy_token(session['login'], vacancy['vacancy_id'])
        if expected_token == query:
            seq = []

            return render_template('discover.html')
        else:
            return redirect(f'{request.root_url}auth')
    else:
        return redirect(f'{request.root_url}auth')


@app.route("/api/get_employee_data")
def set_card():
    pass
