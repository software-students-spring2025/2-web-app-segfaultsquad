from flask_login import UserMixin, LoginManager
from bson.objectid import ObjectId

login_manager = LoginManager()


class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']
        self.password = user_doc['password']
        self.favorites = user_doc.get('favorites', [])


def get_user_by_username(username, db):
    return db.users.find_one({'username': username})


@login_manager.user_loader
def load_user(user_id):
    from flask import current_app
    db = current_app.config['db']
    user_doc = db.users.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        return User(user_doc)
    return None


def init_login_manager(app):
    login_manager.init_app(app)
