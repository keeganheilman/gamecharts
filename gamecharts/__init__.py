import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_login import LoginManager


db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI= 'postgresql://gamecharts:gamecharts@localhost/gc'
    )
    db.init_app(app)

    # import Flask Blueprints
    from .views import views
    from .auth import auth

    # register Flask Blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    # import Flask Models
    from .models import User
    # from .models import Play

    # create tables
    create_db_tables(app)    

    # initialize login_manager 
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # get user account from user id 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


def create_db_tables(app):
    # inspector = inspect(db.get_engine(app))

    # if (inspector.has_table("user") &
    #     True):
    #     print("Using existing database tables.")
    # else:
    db.drop_all(app=app)
    db.create_all(app=app)
    print("Initialized the database.")