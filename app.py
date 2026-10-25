"""Flask admin dashboard: login, view/filter attendance, export CSV."""
import io
from functools import wraps

import pandas as pd
from flask import (Flask, Response, flash, redirect, render_template,
                   request, session, url_for)

from database import get_attendance_records, get_users_list

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (request.form["username"] == ADMIN_USERNAME
                and request.form["password"] == ADMIN_PASSWORD):
            session["admin"] = True
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    date = request.args.get("date", "").strip() or None
    roll_no = request.args.get("roll_no", "").strip() or None
    records = get_attendance_records(date, roll_no)
    users = get_users_list()
    return render_template("dashboard.html", records=records, users=users,
                           date=date or "", roll_no=roll_no or "")


@app.route("/export")
@login_required
def export_csv():
    date = request.args.get("date", "").strip() or None
    roll_no = request.args.get("roll_no", "").strip() or None
    records = get_attendance_records(date, roll_no)
    df = pd.DataFrame(records, columns=["Name", "Roll No", "Date", "Time"])
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return Response(buffer.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=attendance.csv"})


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
