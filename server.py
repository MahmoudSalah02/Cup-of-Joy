"""
Main module of the server file
"""
from flask import render_template
from config.config import *

# Read the swagger files to configure the endpoints
connex_app.add_api("operation.yml")
connex_app.add_api("shop.yml")


# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    return render_template("about.html")


if __name__ == "__main__":
    connex_app.run(debug=True)
