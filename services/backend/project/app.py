import connexion
from project.auth import validate
from project import init_db


def create_app():
    """
    Create app
    :return: Flask app
    """

    connex_app = connexion.FlaskApp(__name__, specification_dir="api_definition/")

    # every HTTP request should be validated before an output is returned
    connex_app.app.before_request(validate.validate_token)

    connex_app.add_api("operation.yaml")
    connex_app.add_api("shop.yaml")
    connex_app.add_api("auth.yaml")

    init_db.init_db()

    @connex_app.route('/', methods=['GET'])
    def index():
        return 'Congratulations! Your API is working'

    return connex_app