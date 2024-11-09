from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Function to create/connect to the database
def init_db():
    with sqlite3.connect("attendance.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_name TEXT NOT NULL,
                            date TEXT NOT NULL,
                            status TEXT NOT NULL
                        )''')
        conn.commit()

# Route to display the attendance page
@app.route('/')
def index():
    return render_template("index.html")

# Route to record attendance
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if request.method == 'POST':
        student_name = request.form['student_name']
        status = request.form['status']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with sqlite3.connect("attendance.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO attendance (student_name, date, status) VALUES (?, ?, ?)", 
                           (student_name, date, status))
            conn.commit()
        
        return redirect(url_for('index'))

# Route to view attendance records
@app.route('/view_attendance')
def view_attendance():
    with sqlite3.connect("attendance.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM attendance")
        records = cursor.fetchall()
    return render_template("attendance_records.html", records=records)

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
