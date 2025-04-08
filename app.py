import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///pbt.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    id = session["user_id"]
    total_income = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'income'", id)[0]["COALESCE(SUM(amount), 0)"]
    total_expenses = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'expense'", id)[0]["COALESCE(SUM(amount), 0)"]
    net_balance = total_income - total_expenses

    rent = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Rent'", id)[0]["COALESCE(SUM(amount), 0)"]
    transportation = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Transportation'", id)[0]["COALESCE(SUM(amount), 0)"]
    food = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Food'", id)[0]["COALESCE(SUM(amount), 0)"]
    others1 = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'expense' AND category = 'Others'", id)[0]["COALESCE(SUM(amount), 0)"]
    salary = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Salary'", id)[0]["COALESCE(SUM(amount), 0)"]
    investment = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Investment'", id)[0]["COALESCE(SUM(amount), 0)"]
    others2 = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'income' AND category = 'Others'", id)[0]["COALESCE(SUM(amount), 0)"]

    return render_template("index.html", total_income=total_income, total_expenses=total_expenses, net_balance=net_balance, rent=rent,
                           transportation=transportation, food=food, others1=others1, others2=others2,salary=salary, investment=investment)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM user WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must provide confirmation password", 400)
        if password != confirmation:
            return apology("password and confirmation password must be same", 400)

        try:
            password = generate_password_hash(password)

            db.execute("INSERT INTO user (username, hash) VALUES(?, ?)", username, password)

            user = db.execute("SELECT id FROM user WHERE username = ?", username)
            session["user_id"] = user[0]["id"]

            return redirect("/")

        except ValueError:
            return apology("username already exists", 400)

    else:
        return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        id = session["user_id"]
        type = request.form.get("type")
        date = request.form.get("date")
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        if not type:
            return apology("Type required", 400)
        if not amount:
            return apology("Amount required", 400)
        if not date:
            return apology("Date required", 400)
        if not category:
            return apology("Category required", 400)

        db.execute("INSERT INTO books(user_id, type, amount, date, category, description) VALUES(?, ?, ?, ?, ?, ?)", id, type, amount, date, category, description)
        return redirect("/add")

    else:
        return render_template("add.html")

@app.route("/view", methods=["GET", "POST"])
@login_required
def view():
    id = session["user_id"]
    if request.method == "POST":
        description = request.form.get("description")
        income = request.form.get("income")
        expense = request.form.get("expense")
        category = request.form.get("category")
        if description:
            rows = db.execute("SELECT * FROM books WHERE user_id = ? AND description LIKE ?", id, f"%{description}%")
            return render_template("view.html",rows=rows)
        elif income:
            rows = db.execute("SELECT * FROM books WHERE user_id = ? AND type = ?", id, income)
            return render_template("view.html",rows=rows)
        elif expense:
            rows = db.execute("SELECT * FROM books WHERE user_id = ? AND type = ?", id, expense)
            return render_template("view.html",rows=rows)
        elif category:
            rows = db.execute("SELECT * FROM books WHERE user_id = ? AND category = ?", id, category)
            return render_template("view.html",rows=rows)
        else:
            return redirect("/view")

    else:
        rows = db.execute("SELECT * FROM books WHERE user_id = ?", id)
        return render_template("view.html", rows=rows)

@app.route("/stat", methods=["GET", "POST"])
@login_required
def stat():
    id = session["user_id"]
    total_income = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'income'", id)[0]["COALESCE(SUM(amount), 0)"]
    total_expenses = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'expense'", id)[0]["COALESCE(SUM(amount), 0)"]
    net_savings = total_income - total_expenses

    rent = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Rent'", id)[0]["COALESCE(SUM(amount), 0)"]
    transportation = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Transportation'", id)[0]["COALESCE(SUM(amount), 0)"]
    food = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Food'", id)[0]["COALESCE(SUM(amount), 0)"]
    others1 = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'expense' AND category = 'Others'", id)[0]["COALESCE(SUM(amount), 0)"]
    salary = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Salary'", id)[0]["COALESCE(SUM(amount), 0)"]
    investment = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND category = 'Investment'", id)[0]["COALESCE(SUM(amount), 0)"]
    others2 = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'income' AND category = 'Others'", id)[0]["COALESCE(SUM(amount), 0)"]

    return render_template("stat.html", total_income=total_income, total_expenses=total_expenses, net_savings = net_savings, rent=rent,
                           transportation=transportation, food=food, others1=others1, others2=others2, salary=salary, investment=investment)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    id = session["user_id"]
    username = db.execute("SELECT username FROM user WHERE id = ?", id)[0]["username"]
    total_income = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'income'", id)[0]["COALESCE(SUM(amount), 0)"]
    total_expenses = db.execute("SELECT COALESCE(SUM(amount), 0) FROM books WHERE user_id = ? AND type = 'expense'", id)[0]["COALESCE(SUM(amount), 0)"]

    return render_template("profile.html", total_income=total_income, total_expenses=total_expenses, username=username)

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    id = request.args.get("delete")
    user_id = session["user_id"]
    db.execute("DELETE FROM books WHERE id = ? AND user_id = ?", id, user_id)
    return redirect("/view")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Get stock quote."""
    if request.method == "POST":
        current = request.form.get("current")
        new = request.form.get("new")
        confirm = request.form.get("confirm")

        if not current:
            return apology("please input Current password", 400)
        if not new:
            return apology("please input New password", 400)
        if not confirm:
            return apology("please input confirm password", 400)
        if new != confirm:
            return apology("New and confirm password must be same", 400)

        id = session["user_id"]
        rows = db.execute("SELECT hash FROM user WHERE id = ?", id)
        if not check_password_hash(
                rows[0]["hash"], current):
            return apology("invalid current password", 403)

        password = generate_password_hash(new)
        db.execute("UPDATE user SET hash = ? WHERE id = ? ", password, id)
        return redirect("/")

    else:
        return render_template("change.html")
