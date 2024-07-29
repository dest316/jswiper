from flask import Flask


app = Flask(__name__)
app.config['DATABASE'] = 'jswiper_db.db'
app.config['SECRET_KEY'] = '9e9ca29fa331a7360d3d25f60c9007c7'
import controllers.main, controllers.api, controllers.auth, controllers.company_profile, controllers.discover
