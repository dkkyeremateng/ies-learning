from app import app, db
from flask import render_template, redirect, session, request, url_for
from user.forms import RegisterForm, LoginForm
from user.models import User
from user.decorators import login_required, admin_required


@app.route('/admin/login/', methods=("POST", "GET"))
def login_page():
    form = LoginForm()

    if request.method == "GET" and request.args.get("next"):
        session["next"] = request.args.get("next")

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                session["username"] = form.username.data
                session["is_author"] = user.is_author
                if "next" in session:
                    next_page = session.get("next")
                    session.pop("next")
                    return redirect(next_page)
                return redirect(url_for("admin"))
            else:
                error = "Invalid password"
                return render_template("user/login.html", form=form, error=error)
        else:
            error = "Invalid username"
            return render_template("user/login.html", form=form, error=error)
    return render_template("user/login.html", form=form)


@app.route('/editor/register', methods=('GET', 'POST'))
@login_required
@admin_required
def register_page():

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(form.fullname.data, form.email.data, form.username.data, form.password.data, True, False)
            session["username"] = form.username.data
            return redirect(url_for("login_page"))
        except Exception as e:
            db.session.rollback()
            print(e)
            error = "Choose a unique username and email"
            return render_template("user/createeditor.html", form=form, error=error)
    return render_template('user/createeditor.html', form=form)


@app.route('/admin/user/', methods=('GET', 'POST'))
def register_admin():

    user_from_db = User.query.filter_by(admin=True).count()

    if user_from_db:
        return redirect(url_for("login_page"))

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(form.fullname.data, form.email.data, form.username.data, form.password.data, True, True)
            session["username"] = form.username.data
            return redirect(url_for("login_page"))
        except Exception as e:
            db.session.rollback()
            print(e)
            error = "Choose a unique username and email"
            return render_template("user/createadmin.html", form=form, error=error)
    return render_template('user/createadmin.html', form=form)


@app.route("/admin/")
@login_required
def admin():
    return render_template("user/admin.html")


@app.route("/logout/")
def logout():
    session.pop("username")
    session.pop("is_author")
    return redirect(url_for("index"))


@app.route('/success/')
@login_required
def success_page():
    return render_template("blog/index.html")
