from app import app
from flask import url_for, request, render_template, redirect, session, abort, jsonify
from models.company_profile_model import get_vacancy, get_vacancy_by_token
from utils import get_db_connection, generate_vacancy_token
from models.discover_model import get_chatted_users, get_random_employee, get_employee_by_id


@app.route('/searching/<query>')
def index(query):
    conn = get_db_connection()
    vacancy = get_vacancy_by_token(conn, query)
    if vacancy and "login" in session:
        expected_token = generate_vacancy_token(session['login'], vacancy['vacancy_id'])
        if expected_token == query:
            if "last_users_id" not in session:
                session["last_users_id"] = {}
            if expected_token not in session["last_users_id"]:
                employee = get_random_employee(conn)
                session["last_users_id"][expected_token] = employee["employee_id"]
            else:
                employee = session["last_users_id"][expected_token]
            return render_template('discover.html', employee=employee)
        else:
            return redirect(f'{request.root_url}auth')
    else:
        return redirect(f'{request.root_url}auth')


@app.route("/api/get_employee_data")
def set_card():
    pass


@app.route("/api/load_employee", methods=["POST"])
def load_employee():
    conn = get_db_connection()
    chatted_users = get_chatted_users(conn, request.json["token"])
    current_employee = get_employee_by_id(session["last_users_id"].get(request.json["token"]), conn)
    if current_employee.size == 0:
        current_employee = get_random_employee(conn)
    else:
        current_employee = current_employee.iloc[0].to_dict()
    print(chatted_users)
    return jsonify({"users": [{"name": user["name"], "description": user["description"]} for _, user in chatted_users.iterrows()],
                    "current_employee": current_employee})
