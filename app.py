from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from functools import wraps
from random import shuffle
from copy import deepcopy


app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///final.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def register_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None or session.get("user_id") == 0:
            return redirect("/register")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():

    session.clear()

    session["user_id"] = 0

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        if session["user_id"] != -1:

            if not request.form.get("username"):

                return render_template("register.html", placeholder="Please provide username")

            if request.form.get("username") == 'admin':

                session["user_id"] = -1

                return redirect("/register")

            db.execute("INSERT INTO entries (username, score, completed) VALUES (?, 0, 'false')", request.form.get("username"))

            session["user_id"] = db.execute("SELECT * FROM entries WHERE username = ? ORDER BY id DESC", request.form.get("username"))[0]["id"]

            return redirect("/quiz")

        else:

            if not request.form.get("password"):

                return render_template("register.html", placeholder="Please provide password")

            if request.form.get("password") != db.execute("SELECT password FROM admin WHERE id = 1")[0]["password"]:

                return render_template("register.html", placeholder="Incorrect password")

            session["user_id"] = db.execute("SELECT id FROM admin WHERE username = 'admin'")[0]["id"]

            return redirect("/questions")

    else:

        try:

            if session["user_id"] == -1:

                return render_template("register.html", placeholder="")

            else:

                return render_template("register.html", placeholder="")

        except KeyError:

            session["user_id"] = 0

            return render_template("register.html", placeholder="")



@app.route("/logout")
def logout():

    db.execute("DELETE FROM entries WHERE id = ? AND completed = 'false'", session["user_id"])

    session.clear()

    return redirect("/")


@app.route("/questions", methods=['GET', 'POST'])
@register_required
def questions():

    if session["user_id"] != 1:

        session.clear()

        return redirect("/")

    if request.method == 'POST':

        if request.form.get("delete") == "delete":

            db.execute("DELETE FROM questions")

        else:

            db.execute("DELETE FROM questions WHERE id = ?", request.form.get("id"))

    questions = db.execute("SELECT * FROM questions")

    return render_template("questions.html", questions=questions)


@app.route("/add", methods=['GET', 'POST'])
@register_required
def add():

    if session["user_id"] != 1:

        session.clear()

        return redirect("/")

    if request.method == "POST":

        question = request.form.get("question")
        correct = request.form.get("canswer")
        wrong1 = request.form.get("wanswer1")
        wrong2 = request.form.get("wanswer2")
        wrong3 = request.form.get("wanswer3")

        if not (question and correct and wrong1 and wrong2 and wrong3):
            return render_template("add.html", placeholder="Provide question and/or answer/s")

        db.execute("INSERT INTO questions (text, correct, total, answer, wanswer1, wanswer2, wanswer3) VALUES (?, 0, 0, ?, ?, ?, ?)", question, correct, wrong1, wrong2, wrong3)

        return redirect("/questions")

    else:

        return render_template("add.html", placeholder="")


@app.route("/statistic", methods=['GET', 'POST'])
@register_required
def statistic():

    if session["user_id"] == 1:

        admin = True

    else:

        admin = False

    if request.method == 'POST':

        if request.form.get("delete") == "delete":

            db.execute("DELETE FROM entries WHERE id <> 1")

        else:

            db.execute("DELETE FROM entries WHERE id = ?", request.form.get("id"))

    entries = db.execute("SELECT * FROM entries WHERE completed = 'true' AND id <> 1")

    noq = db.execute("SELECT COUNT(*) FROM questions")[0]["COUNT(*)"]

    return render_template("statistic.html", entries=entries, noq=noq, admin=admin)


@app.route("/quiz", methods=['GET', 'POST'])
@register_required
def quiz():

    if session["user_id"] == 1:

        session.clear()

        return redirect("/")

    if request.method == 'GET':

        db.execute("DELETE FROM temp")

        questions = db.execute("SELECT * FROM questions")

        completed = db.execute("SELECT completed FROM entries WHERE id = ?", session["user_id"])[0]["completed"]

        shuffle(questions)

        for question in questions:

            db.execute("INSERT INTO temp (id, text, answer, wanswer1, wanswer2, wanswer3) VALUES (?, ?, ?, ?, ?, ?)", question["id"], question["text"], question["answer"], question["wanswer1"], question["wanswer2"], question["wanswer3"])

        return render_template("quiz.html", started=False, index=1, completed=completed)

    else:

        index = int(request.form.get("index"))

        questions = db.execute("SELECT * FROM temp")

        question = questions[index - 1]

        if request.form.get("quiz") == None:

            placeholder = "Please provide an answer"

            index -= 1

        else:

            placeholder = ""

            if request.form.get("quiz") != 'start':

                print(question["answer"])

                print(request.form.get("quiz"))

                if question["answer"] == request.form.get("quiz"):

                    score = db.execute("SELECT score FROM entries WHERE id = ?", session["user_id"])[0]["score"]

                    db.execute("UPDATE entries SET score = ? WHERE id = ?", score + 1, session["user_id"])

                    correct = db.execute("SELECT correct FROM questions WHERE id = ?", question["id"])[0]["correct"]

                    db.execute("UPDATE questions SET correct = ? WHERE id = ?", correct + 1, question["id"])

                total = db.execute("SELECT total FROM questions WHERE id = ?", question["id"])[0]["total"]

                db.execute("UPDATE questions SET total = ? WHERE id = ?", total + 1, question["id"])

            else:

                db.execute("UPDATE entries SET score = 0 WHERE id = ?", session["user_id"])

                db.execute("UPDATE entries SET completed = 'false' WHERE id = ?", session["user_id"])

        if index == db.execute("SELECT COUNT(*) FROM temp")[0]["COUNT(*)"]:

            db.execute("UPDATE entries SET completed = 'true' WHERE id = ?", session["user_id"])

            return redirect("/statistic")

        question = questions[index]

        choices = [None] * 4

        choices[0] = question["answer"]
        choices[1] = question["wanswer1"]
        choices[2] = question["wanswer2"]
        choices[3] = question["wanswer3"]

        shuffle(choices)

        return render_template("quiz.html", started=True, question=question, choices=choices, index=index + 1, placeholder=placeholder)