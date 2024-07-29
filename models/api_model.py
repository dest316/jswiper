import sqlite3
import pandas as pd


def get_company_amount(conn):
    return int(pd.read_sql(f'''SELECT COUNT (*) as cnt FROM companies;''', conn).iloc[0]['cnt'])


def add_new_user(conn, name, login, password):
    try:
        cur = conn.cursor()
        query = '''INSERT INTO companies (company_name, company_login, company_password) VALUES (?, ?, ?)'''
        cur.execute(query, (name, login, password))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e.sqlite_errorcode)
    return False


def check_exist_user(conn, login):
    return pd.read_sql(f'''SELECT * FROM companies WHERE company_login = ?''', conn, params=[login]).size == 0


def check_auth_data(conn, login, password):
    return pd.read_sql(f'''SELECT * FROM companies 
    WHERE company_login = ? AND company_password = ?''',
                       conn, params=[login, password]).size > 0
