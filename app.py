from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ================= DATABASE CONNECTION =================
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )

# ================= AUTH =================

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if admin:
        session['admin'] = admin['username']
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials"

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('index'))
    return render_template("admin_dashboard.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ================= STUDENTS =================

@app.route('/students')
def students_page():
    if 'admin' not in session:
        return redirect(url_for('index'))
    return render_template("student.html")

@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (admission, name, grade) VALUES (%s, %s, %s)",
        (data['admission'], data['name'], data['grade'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Student added"})

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Deleted"})

# ================= TEACHERS =================

@app.route('/teachers')
def teachers_page():
    if 'admin' not in session:
        return redirect(url_for('index'))
    return render_template("teacher.html")

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(teachers)

@app.route('/api/teachers', methods=['POST'])
def add_teacher():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO teachers (tsc, name, subject, phone, email) VALUES (%s, %s, %s, %s, %s)",
        (data['tsc'], data['name'], data['subject'], data['phone'], data['email'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Teacher added"})

@app.route('/api/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)