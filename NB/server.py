from flask import render_template, session,redirect, request
from flask_app import app
from flask_app.controllers.users import User
from flask_app.controllers.adventures import Adventure



if __name__ == "__main__":
    app.run(debug=True, port=5005)