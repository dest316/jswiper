import random

import pandas as pd


def get_random_employee(conn, vacancy_hash):
    employee = pd.read_sql(f'''
    SELECT * 
FROM (
    WITH AnswerVacancy AS (
        SELECT * FROM answers
        JOIN vacancies ON answers.vacancy_id = vacancies.vacancy_id AND vacancy_hash = '{vacancy_hash}'
    )
    SELECT * 
    FROM employees 
    LEFT JOIN AnswerVacancy USING (employee_id)
    WHERE answer_last_timestamp IS NULL 
       OR (CAST(strftime("%s", "now") AS NUMERIC) - answer_last_timestamp > 180)
) 
ORDER BY RANDOM() 
LIMIT 1;
    ''', conn)
    print(employee)
    if employee.empty:
        return None
    return employee.iloc[0].to_dict()


def get_employee_by_id(employee_id, conn):
    if employee_id is None:
        return None
    return pd.read_sql(f'''
    SELECT * FROM employees WHERE employee_id = "{employee_id}"''', conn)


def get_chatted_users(conn, vacancy_hash):
    return pd.read_sql(f'''SELECT employee_full_name AS name, employee_description AS description
    FROM answers
    JOIN vacancies USING (vacancy_id)
    JOIN employees USING (employee_id)
    WHERE vacancy_hash = "{vacancy_hash}";''', conn)


def set_answer(conn, **data):
    cur = conn.cursor()
    query = '''
        INSERT OR REPLACE INTO answers (vacancy_id, employee_id, answer_last_timestamp, answer_result)
        VALUES (?, ?, CAST(strftime("%s", "now") AS NUMERIC), ?);
        '''
    cur.execute(query, (data.get('vacancy_id'), data.get('employee_id'), data.get('result')))
    conn.commit()

