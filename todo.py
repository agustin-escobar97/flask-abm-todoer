from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint("todo", __name__)

@bp.route("/")
@login_required
def index():
    db, c = get_db()
    c.execute ("SELECT todo.id, todo.description, todo.created_by FROM prueba.todo WHERE created_by = %s ORDER BY todo.id DESC;", (g.user["id"],))

    todos = c.fetchall()

    return render_template("todo/index.html", todos=todos)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        description = request.form["description"]
        error = None

        if description is None:
            error("La descripción está vacía")
        
        if error is not None:
            flash(error)

        else:
            db, c = get_db()
            c.execute ("INSERT INTO todo (description, created_by) VALUES (%s, %s);", (description, g.user["id"]))
            db.commit()
            return redirect(url_for("todo.index"))

    return render_template("todo/create.html")

def get_todo(id):
    db, c = get_db()
    c.execute("SELECT todo.id, todo.description, todo.completed, todo.created_by, todo.created_at, user.username FROM todo JOIN user on todo.created_by = user.id WHERE todo.id = %s;", (id,))

    todo = c.fetchone()

    if todo == None:
    	abort(404, "El todo de ID {0} no existe".format(id)) 

    return todo

@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == "POST":
        description = request.form["description"]
        completed = True if request.form.get("completed") == "on" else False
        error = None

        if not description:
            error = "Description se encuentra vacio"

        if error is not None:
            flash(error)
        
        else:
            db, c = get_db()
            c.execute("UPDATE todo SET DESCRIPTION = %s, completed = %s WHERE id = %s", (description, completed, id))
            db.commit()
            return redirect(url_for("todo.index"))

    return render_template("todo/update.html", todo=todo)

@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    todo = get_todo(id)
    db, c = get_db()
    c.execute("DELETE FROM todo WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for("todo.index"))