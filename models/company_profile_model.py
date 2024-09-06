import pandas as pd



def get_company(conn, login):
    return pd.read_sql('SELECT * FROM companies WHERE company_login = ?', conn, params=[login])


def get_vacancies(conn, company_login):
    return pd.read_sql('''SELECT * FROM companies 
    JOIN vacancies USING (company_id) WHERE company_login = ?''', conn, params=[company_login])


def get_owners_login(conn, vacancy_id):
    df = pd.read_sql(f'''SELECT company_login FROM companies
JOIN vacancies USING (company_id) WHERE vacancy_id = ?''', conn, params=[vacancy_id])
    if df.empty:
        return None
    return df.iloc[0]['company_login']


def delete_vacancy(conn, vacancy_id):
    cur = conn.cursor()
    cur.execute(f'''DELETE FROM vacancies WHERE vacancy_id = {vacancy_id}''')
    conn.commit()


def get_vacancy(conn, vacancy_id):
    df = pd.read_sql('''SELECT * FROM vacancies
    WHERE vacancy_id = ?''', conn, params=[vacancy_id])
    return None if df.empty else df.iloc[0].to_dict()


def get_vacancy_by_token(conn, vacancy_token):
    df = pd.read_sql('''SELECT * FROM vacancies
    WHERE vacancy_hash = ?''', conn, params=[vacancy_token])
    return None if df.empty else df.iloc[0].to_dict()

def get_company_id_by_login(conn, login):
    return pd.read_sql('''SELECT company_id FROM companies
    WHERE company_login = ?''', conn, params=[login]).iloc[0]['company_id']


def get_vacancies_columns_names(conn):
    df = pd.read_sql('''SELECT * FROM vacancies LIMIT 1''', conn)
    return df.columns.to_list()


def update_vacancy(conn, vacancy_id, values):
    cur = conn.cursor()
    set_query_part = ','.join([f'{i[0]} = "{i[1]}"' for i in values.items()])
    cur.execute(f'''UPDATE vacancies SET {set_query_part} WHERE vacancy_id = {vacancy_id}''')
    conn.commit()


def add_vacancy(conn, company_id, values):
    cur = conn.cursor()
    columns_part = 'company_id,' + ','.join(values.keys())
    values_part = f'{company_id},' + ','.join(map(lambda x: f'"{x}"' if '"' not in x else f'"{x.replace('"', '\'')}"', values.values()))
    cur.execute(f'''INSERT INTO vacancies ({columns_part}) VALUES ({values_part})''')
    conn.commit()
    return cur.lastrowid
