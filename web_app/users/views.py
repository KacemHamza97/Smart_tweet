import json
from flask_mail import Message
import requests
from flask import Blueprint, render_template, url_for, request, session, redirect
from flask_login import logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from web_app import db, mail
from web_app.models import User

user = Blueprint('user', __name__, template_folder='templates/users', static_folder='static')


@user.route('/', methods=['Get', 'POST'])
def index():
    posts = db.posts
    all_posts = posts.find()
    return render_template('index.html', all_posts=all_posts)


@user.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        msg = Message(request.form['subject'], recipients=['zarzouut@gmail.com'], sender=request.form.get("email"))
        # msg.body = request.form['message']
        msg.html = request.form['message'] + "<br><br>" + '<b style="color: red;" >' + \
                   "sent by: " + request.form.get("email") + '</b>'
        mail.send(msg)

    return render_template('contact.html')


@user.route('/aboutUs')
def aboutus():
    return render_template('aboutus.html')


@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user:
            if check_password_hash(existing_user['password'], request.form['password']):
                login_user(User(existing_user))
                session['username'] = request.form['username']
                return redirect(url_for('user.index'))
    return render_template('login.html')


@user.route('/register', methods=['POST', 'GET'])
def register():
    """ This Router handle registration action

    """
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'username': request.form['username']})
        print(existing_user)
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': '6Le9ZrMZAAAAAIxnKN_Cfz7MXT70GuBXmnd0GWrN',
                                'response': request.form['g-recaptcha-response']})
        google_response = json.loads(r.text)
        if existing_user is None:
            hashpass = generate_password_hash(request.form['password'])
            users.insert({'username': request.form['username'], 'password': hashpass, 'email': request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('user.index'))

        return 'That username already exists!'

    return render_template('register.html')


@user.route("/user_logout")
def user_logout():
    logout_user()
    session.clear()
    return redirect(url_for('user.index'))

# cle :6Lf-ZbMZAAAAACq-9qgRBhcTTmdGEbDeMo7LzqgT
# 6Lf-ZbMZAAAAACN9vFu548Gnb_Xm7_PcNeooQfk8
