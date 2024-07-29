from app import app
from flask import render_template, request, session, jsonify, abort, redirect
from utils import get_db_connection, generate_vacancy_token
from models.company_profile_model import get_company, get_vacancies, get_owners_login, delete_vacancy, get_vacancy, get_vacancies_columns_names, update_vacancy, add_vacancy, get_company_id_by_login


@app.route('/api/get_vacancies', methods=["POST"])
def get_vacancies_list():
    conn = get_db_connection()
    df = get_vacancies(conn, session['login'])
    return jsonify({'vacancies': df.to_json(orient='records')})


@app.route('/api/delete_vacancy', methods=["POST"])
def delete_required_vacancy():
    conn = get_db_connection()
    true_owner = get_owners_login(conn, request.json['vacancy_id'])
    if true_owner is not None and true_owner == session['login']:
        delete_vacancy(conn, request.json['vacancy_id'])
        return jsonify({'result': 'ok'})
    else:
        abort(403)


@app.route('/home/<string:login>')
def profile(login):
    if 'login' not in session:
        return redirect(f'{request.root_url}auth')
    conn = get_db_connection()
    company = get_company(conn, login).iloc[0]
    return render_template('company_profile.html',
                           company_name=company.company_name)


@app.route('/api/get_vacancy_info', methods=["POST"])
def get_vacancy_info():
    conn = get_db_connection()
    if request.json['vacancy_id'] is None:
        columns = list(filter(lambda x: not x.endswith('_id') and not x.endswith('_hash'), get_vacancies_columns_names(conn)))
        return jsonify({'columns': columns})
    true_owner = get_owners_login(conn, request.json['vacancy_id'])
    if true_owner is not None and true_owner == session['login']:
        info = {k: v for k, v in get_vacancy(conn, request.json['vacancy_id']).items() if not k.endswith('_id') and not k.endswith('_hash')}
        return jsonify(info)
    else:
        abort(403)


@app.route('/api/update_vacancy', methods=["PUT", "POST"])
def update_vacancy_data():
    conn = get_db_connection()
    columns = get_vacancies_columns_names(conn)
    gotten_columns = request.json['data'].keys()
    if not set(gotten_columns).issubset(set(columns)):
        abort(400)
    if request.method == 'PUT':
        true_owner = get_owners_login(conn, request.json['vacancy_id'])
        if true_owner is not None and true_owner == session['login']:
            update_vacancy(conn, request.json['vacancy_id'], request.json['data'])
            return jsonify({'result': 'ok'})
        else:
            abort(403)
    if request.method == 'POST':
        # To-do: При добавлении новой вакансии на нее нельзя сразу перейти, работает только после перезагрузки страницы
        last_row_id = add_vacancy(conn, get_company_id_by_login(conn, session['login']), request.json['data'])
        update_vacancy(conn, last_row_id, {'vacancy_hash': generate_vacancy_token(session['login'], last_row_id)})
        return jsonify({'result': 'ok', 'new_id': last_row_id})
