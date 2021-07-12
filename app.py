import os
from datetime import datetime

from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = "sqlite:///{}".format(os.path.join(BASE_DIR, "todo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_FILE
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    done = db.Column(db.Boolean)
    date = db.Column(db.DateTime, default=datetime.now())


def create_todo(text):
    todo = Todo(text=text)
    db.session.add(todo)
    db.session.commit()
    db.session.refresh(todo)


def read_todos():
    return db.session.query(Todo).all()


def update_todo(todo_id, text, done):
    db.session.query(Todo).filter_by(id=todo_id).update({
        "text": text,
        "done": True if done == "on" else False
    })
    db.session.commit()


def delete_todo(todo_id):
    db.session.query(Todo).filter_by(id=todo_id).delete()
    db.session.commit()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        create_todo(request.form["text"])
    return render_template("index.html", todos=read_todos())


@app.route("/edit/<todo_id>", methods=["POST", "GET"])
def edit_todo(todo_id):
    if request.method == "POST":
        update_todo(todo_id, text=request.form['text'], done=request.form['done'])
    elif request.method == "GET":
        delete_todo(todo_id)
    return redirect("/", code=302)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
