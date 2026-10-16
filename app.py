from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-for-real-deployment"
DB_PATH = Path(__file__).with_name("college_erp.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            roll_no TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            attended INTEGER NOT NULL,
            total INTEGER NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        );
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            time TEXT NOT NULL,
            subject TEXT NOT NULL,
            room TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            exam_time TEXT NOT NULL,
            venue TEXT NOT NULL
        );
        """)
        if db.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
            db.execute("INSERT INTO students(username,password,full_name,roll_no) VALUES(?,?,?,?)",
                       ("student", "student123", "Demo Student", "ERP-001"))
            sid = db.execute("SELECT id FROM students WHERE username='student'").fetchone()[0]
            db.executemany("INSERT INTO attendance(student_id,subject,attended,total) VALUES(?,?,?,?)", [
                (sid, "Database Management", 22, 25),
                (sid, "Data Science", 24, 28),
                (sid, "Operating Systems", 18, 23)
            ])
        if db.execute("SELECT COUNT(*) FROM timetable").fetchone()[0] == 0:
            db.executemany("INSERT INTO timetable(day,time,subject,room) VALUES(?,?,?,?)", [
                ("Monday", "09:00 - 10:00", "Database Management", "Lab 2"),
                ("Monday", "10:15 - 11:15", "Data Science", "Room 204"),
                ("Monday", "11:30 - 12:30", "Operating Systems", "Room 108"),
            ])
        if db.execute("SELECT COUNT(*) FROM exams").fetchone()[0] == 0:
            db.executemany("INSERT INTO exams(subject,exam_date,exam_time,venue) VALUES(?,?,?,?)", [
                ("Database Management", "2026-10-24", "10:00 AM", "Hall A"),
                ("Data Science", "2026-10-27", "10:00 AM", "Hall B"),
                ("Operating Systems", "2026-10-30", "02:00 PM", "Hall A"),
            ])

@app.route("/")
def home():
    if not session.get("student_id"):
        return redirect(url_for("login"))
    with get_db() as db:
        student = db.execute("SELECT * FROM students WHERE id=?", (session["student_id"],)).fetchone()
        attendance = db.execute("SELECT * FROM attendance WHERE student_id=?", (student["id"],)).fetchall()
        timetable = db.execute("SELECT * FROM timetable ORDER BY id").fetchall()
        exams = db.execute("SELECT * FROM exams ORDER BY exam_date").fetchall()
    return render_template("dashboard.html", student=student, attendance=attendance, timetable=timetable, exams=exams)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        with get_db() as db:
            student = db.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password)).fetchone()
        if student:
            session["student_id"] = student["id"]
            return redirect(url_for("home"))
        flash("Incorrect username or password. Try the demo credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
