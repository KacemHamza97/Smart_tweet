from flask import Flask
from flask_login import LoginManager
from flask_recaptcha import ReCaptcha
from pymongo import MongoClient
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le9ZrMZAAAAADc_WhUSS_JTDMHTPqE-KbFvVrv7'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le9ZrMZAAAAAIxnKN_Cfz7MXT70GuBXmnd0GWrN'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}
recaptcha = ReCaptcha(app=app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'zarzouut@gmail.com'
app.config['MAIL_PASSWORD'] = '199719971997'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

client = MongoClient('mongodb://localhost:27017/')
db = client.news

from web_app.users.views import user

app.register_blueprint(user)
