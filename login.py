from flask import render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import auth


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")


def find_auth_module():
    auth_dir = os.environ.get("AUTH_DIR")
    if not auth_dir:
        print("AUTH_DIR not set.")
        return None

    auth_module_path = os.path.join(auth_dir, "auth.py")

    if os.path.isfile(auth_module_path):
        print("Auth module file found at:", auth_module_path)
        return auth_module_path

    print("Auth module file not found.")
    return None


def register(app):

    @app.route("/", methods=["GET", "POST"])
    def login():

        form = LoginForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            password = form.password.data

            branch, fullname = auth.authenticate(username, password)

            if branch:
                session["username"] = username
                session["branch"] = branch
                session["fullname"] = fullname
                return redirect(url_for("dashboard"))

            return render_template(
                "login.html", form=form, error="Invalid username or password"
            )

        return render_template("login.html", form=form)
