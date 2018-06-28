#-*- coding: utf-8 -*-

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.mongoengine import MongoEngine
import jinja2
import os
from werkzeug.contrib.cache import SimpleCache


class SystemCache(SimpleCache):

    def __init__(self, threshold=500, default_timeout=300):
        super(SystemCache, self).__init__(threshold, default_timeout)

    def get_model(self, key, function=None):
        val = super(SystemCache, self).get(key)
        if val is None and function is not None:
            val = function()
            self.set(key, function())
        return val

app = Flask(__name__, static_url_path='/static')

app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.PackageLoader('flask_admin'),
    jinja2.PackageLoader('mosca'),
    jinja2.FileSystemLoader([
        '/templates/mosca/',
        '/templates/admin/',
        '/templates/tools/',
    ]),
])

cache = SystemCache()
app.config['DEBUG'] = True
app.config["MONGODB_SETTINGS"] = {
    'DB': "fried_bundle_fly",
    'HOST': '127.0.0.1',
    'PORT': 15984,
    'USERNAME': 'clockwork_monster_fly',
    'PASSWORD': '(*&$%@HAGS&dha'
}
app.config['SECRET_KEY'] = 'development key'

#app.config['SESSION_TYPE'] = 'mongodb'
#app.config['SESSION_MONGODB'] = '127.0.0.1:15984'
#app.config['SESSION_MONGODB_DB'] = 'fried_bundle_fly'
#app.config['SESSION_MONGODB_COLLECT'] = 'sessions'
app.config['BASE_DIR'] = os.path.dirname(os.path.realpath(__file__))


def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)
    return dict(format_price=format_price)

app.context_processor(utility_processor)


'''from mosca.views import *
from mosca.models.admin import *
from mosca.models.articles import *
aidmim = Admin(
    app,
    'Aidmim',
    index_view=MyAdminIndexView(url='/aidmim'),
    base_template='admin/mosca_master.html',
)

#articles
aidmim.add_view(ArticleView(Article, db.session))
aidmim.add_view(MyModelView(Category, db.session))

#users
aidmim.add_view(MyModelView(User, db.session))

ToolsViews.register(app)


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

init_login()'''

db = MongoEngine(app)
#admin.init_app(app)


def register_blueprints(app):
    # Prevents circular imports
    from mosca.views.posts import posts
    from mosca.views.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)


'''with app.app_context():
    db.session.commit()
    # passwords are hashed, to use plaintext passwords instead:
    # test_user = User(login="test", password="test")
    user = db.session.query(User)\
        .filter(User.username == 'test').first()
    if user is None:
        test_user = User(
            username="test",
            email="kalkehcoisa@gmail.com",
            password=generate_password_hash("test"))
        db.session.add(test_user)
        db.session.commit()'''

#app.run(debug=True, use_reloader=True, use_debugger=True)
