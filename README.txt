COLLEGE ERP - SPRINT 2 PROTOTYPE (HTML/CSS + FLASK + SQLITE)

This version focuses on the four user stories included in SCRUM Sprint 2:
1. Student Login to College ERP
2. View Student Attendance
3. View Class Timetable
4. View Examination Schedule

Files:
- app.py: Flask backend and routes
- templates/login.html: login page
- templates/dashboard.html: student dashboard and the three sprint features
- static/style.css: website styling
- college_erp.db: SQLite database (created automatically at first run)
- requirements.txt: dependency

RUN LOCALLY:
1. Install Python 3.
2. Open a terminal in this folder.
3. Run: pip install -r requirements.txt
4. Run: python app.py
5. Open http://127.0.0.1:5000

DEMO LOGIN:
Username: student
Password: student123

DATABASE:
SQLite stores demo student login details, attendance rows, timetable rows, and exam schedule rows.
The database is initialized automatically by app.py. Sample data is for demonstration only.

IMPORTANT:
This is an educational prototype, not production-ready authentication. The demo password is stored plainly
for simplicity; do not use this pattern for a real deployment. No actual college system is connected.
The Jira assignment also lists four additional stories (Mark Student Attendance, Upload Study Material,
Manage Student Records, View College Announcements), but these are outside the four stories selected
for SCRUM Sprint 2 in Assignment 2.
