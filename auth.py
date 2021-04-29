import functools
from flask import (Blueprint, flash, g, render_template, request, url_for, session, redirect)
from werkzeug.security import check_password_hash, generate_password_hash
from todo.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute(
            "SELECT id FROM prueba.user WHERE username = %s", (username,)
        )
        if username is None:
            error = "Por favor, introduzca un username"
        if password is None:
            error = "Por favor, ingrese una contraseña"
        elif c.fetchone() is not None:
            error = "Usuario {} se encuentra registrado.".format(username)

        if error is None:
            c.execute("INSERT INTO prueba.user (username, password) values (%s, %s)",
            (username, generate_password_hash(password))
            )
            db.commit()
        
            return redirect(url_for("auth.login"))
    
        flash(error)

    return render_template("auth/register.html") #renderiza el template en vez de recargar la pagina

@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None:
        return redirect(url_for("todo.index")) #en caso de que el usuario ya haya iniciado sesión, será redireccionado al indice
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute("SELECT * FROM prueba.user WHERE username = %s", (username,))
        g.user = c.fetchone()

        if g.user is None:
            error = "Usuario y/o contraseña inválida"
        elif not check_password_hash(g.user["password"], password):
            error = "Usuario y/o contraseña inválida"
        
        if error is None:
            session.clear()
            session["user_id"] = g.user["id"]
            return redirect (url_for("todo.index"))

        flash(error)

    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute("SELECT * FROM prueba.user WHERE id = %s", (user_id,))
        g.user = c.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
