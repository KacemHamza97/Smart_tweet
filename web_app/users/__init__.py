from web_app import login_manager, db
from web_app.models import User


@login_manager.user_loader
def user_loader(id):
    users = db.users
    return User(users.find_one({'_id': id}))


@login_manager.request_loader
def request_loader(request):
    users = db.users
    existing_user = users.find_one({'username': request.form.get('username')})
    return User(existing_user) if existing_user else None