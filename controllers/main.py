from app import app
from flask import render_template
from models.api_model import get_company_amount
from utils import get_db_connection


@app.route('/', methods=["GET", "POST"])
def main():
    start_company_amount = get_company_amount(get_db_connection())
    html = render_template('main.html', start_company_amount=start_company_amount)
    return html
