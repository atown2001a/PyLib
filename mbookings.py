from flask import render_template, session
import json
from pathlib import Path
import fcntl 

BOOKINGS_JSON = Path("/opt/PyPCBookingSystem/data/bookings.json")

# def register(app):
#    @app.route("/mbookings")


def mbookings():
    branch = session["branch"]

    with open(BOOKINGS_JSON, "r", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_SH) 
        try:
            all_bookings = json.load(f)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    branch_bookings = [b for b in all_bookings if b.get("branch") == branch]
    branch_bookings.sort(key=lambda b: (b.get("date", ""), b.get("time", "")))

    return render_template(
        "mbookings.html",
        username=session["username"],
        fullname=session.get("fullname"),
        bookings=branch_bookings,
        branch=branch,
    )
