import random

import pandas as pd


def get_random_employee(conn):
    employee = pd.read_sql('''
    SELECT * 
FROM (
    SELECT * 
    FROM employees 
    LEFT JOIN answers USING (employee_id)
    WHERE answer_last_timestamp IS NULL 
       OR (strftime("%s", "now") - answer_last_timestamp > 180)
) 
ORDER BY RANDOM() 
LIMIT 1;
    ''', conn)
    return employee.iloc[0].to_dict()


def get_employee_by_id(employee_id, conn):
    return pd.read_sql(f'''
    SELECT * FROM employees WHERE employee_id = "{employee_id}"''', conn)


def get_chatted_users(conn, vacancy_hash):
    return pd.read_sql(f'''SELECT employee_full_name AS name, employee_description AS description
    FROM answers
    JOIN vacancies USING (vacancy_id)
    JOIN employees USING (employee_id)
    WHERE vacancy_hash = "{vacancy_hash}";''', conn)
