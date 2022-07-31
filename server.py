import connexion
from flask import render_template
from auth import validate
connex_app = connexion.FlaskApp(__name__, specification_dir="api_definition/")
connex_app.app.before_request(validate.validate_token)

# Read the swagger files to configure the endpoints
connex_app.add_api("operation.yaml")
connex_app.add_api("shop.yaml")
connex_app.add_api("login.yaml")

# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return "Connected"


if __name__ == "__main__":
    connex_app.run(debug=True)

# TODO: write server in this format
# from flask import Flask
#
# from .config import app_config
# from .models import bcrypt
# from createtable import db
#
# from .views.UserView import user_api as user_blueprint
# from .views.BlogpostView import blogpost_api as blogpost_blueprint
#
# env_name = 'development'
#
#
# def create_app(env_name):
#     """
#     Create app
#     """
#
#     # app initiliazation
#     app = Flask(__name__)
#
#     app.config.from_object(app_config[env_name])
#
#     # initializing bcrypt and db
#     bcrypt.init_app(app)
#     db.init_app(app)
#
#     app.register_blueprint(user_blueprint, url_prefix='/users')
#     app.register_blueprint(blogpost_blueprint, url_prefix='/blogposts')
#
#     @app.route('/', methods=['GET'])
#     def index():
#         return 'Congratulations! Your API is working'
#
#     return app
# TODO: put everything inside src and create a file run outside