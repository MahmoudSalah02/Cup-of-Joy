import connexion

# Create the connexion application instance
connex_app = connexion.FlaskApp(__name__, specification_dir="../api_definition/")
