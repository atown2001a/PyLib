from flask import render_template, redirect, url_for, session
import json
from datetime import datetime
import mbookings as mb

def get_due_books(customers):
    today = datetime.today().date()
    due_books = []

    for customer in customers:
        for book in customer["books"]:
            if datetime.strptime(book["due_date"], "%Y-%m-%d").date() <= today:
                due_books.append({
                    "customer": customer["name"],
                    "book": book["title"],
                    "due_date": book["due_date"]
                })

    return due_books


def register(app):
    @app.route("/dashboard")
    def dashboard():
        if "username" in session and "branch" in session:
            branch = session["branch"]

            with open("data/customers.json") as f:
                all_customers = json.load(f)

            customers = [c for c in all_customers if c["branch"] == branch]
            due_books = get_due_books(customers)

            return render_template(
                "dashboard.html",
                username=session["username"],
		fullname=session.get('fullname'),
                branch=branch,
                customers=customers,
                due_books=due_books
            )

        return redirect(url_for("login"))
	
    @app.route("/about")
    def about():
    	return render_template("about.html")

    @app.route("/mbookings")
    def mbookings():
    	return mb.mbookings()

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        session.pop("branch", None)
        return redirect(url_for("login"))
