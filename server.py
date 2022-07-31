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
