from app import app
from utils import get_db_connection
from flask import jsonify, request, session, url_for
from models.api_model import get_company_amount, add_new_user, check_exist_user, check_auth_data


@app.route('/api/company_amount', methods=["POST"])
def company_amount():
    return jsonify({'amount': get_company_amount(get_db_connection())})


@app.route('/api/reg', methods=["POST"])
def registration():
    conn = get_db_connection()
    return jsonify({'result': add_new_user(conn, request.json['name'], request.json['login'], request.json['password'])})


@app.route('/api/check_exist', methods=["POST"])
def check_ex():
    conn = get_db_connection()
    return jsonify({'result': check_exist_user(conn, request.json['login'])})


@app.route('/api/log_in', methods=["POST"])
def logining():
    conn = get_db_connection()
    result = check_auth_data(conn, request.json['login'], request.json['password'])
    if result:
        session['login'] = request.json['login']
    return jsonify({'result': result,
                    'login': request.json['login']})


@app.route('/api/log_out', methods=["POST"])
def logouting():
    conn = get_db_connection()
    del session['login']
    return jsonify({'path': f'{request.root_url}auth'})
