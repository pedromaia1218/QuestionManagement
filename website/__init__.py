from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '6s54da98sd4q6w54edq6847a6g5d4g9'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app