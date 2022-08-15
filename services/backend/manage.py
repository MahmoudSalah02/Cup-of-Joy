# TODO: create a Flask CLI instead of running the application like this:
# from flask.cli import FlaskGroup

from project import app

if __name__ == "__main__":
    app = app.create_app()
    app.run(debug=True)