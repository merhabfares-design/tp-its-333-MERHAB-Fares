from app import app
from flask import request, jsonify
from app.models import get_db
from app.auth import token_required

from flask import render_template, request, redirect, url_for, session

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")

    # POST (formulaire HTML)
    login = request.form.get("login")
    password = request.form.get("password")
    code = request.form.get("code")  # ← IMPORTANT

    if login == "admin" and password == "admin123" and code == "123456":
        session['logged_in'] = True
        return redirect(url_for("home"))

    return render_template("login.html", error="Identifiants ou code incorrects")

@app.route("/", methods=["GET"])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT nom, adresse, pincode FROM students")
    students = c.fetchall()
    conn.close()
    return render_template("new.html", students=students)

@app.route("/students", methods=["POST"])
def add_student():
    if request.is_json:
        # API request - requires token
        return token_required(lambda: _add_student_api())()
    else:
        # Web form request - no token required
        return _add_student_web()

def _add_student_api():
    data = request.get_json()
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO students (nom, adresse, pincode) VALUES (?, ?, ?)",
        (data["nom"], data["adresse"], data["pincode"])
    )
    conn.commit()
    conn.close()
    return jsonify(message="Étudiant ajouté")

def _add_student_web():
    nom = request.form.get("nom")
    adresse = request.form.get("adresse")
    pincode = request.form.get("pincode")
    
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO students (nom, adresse, pincode) VALUES (?, ?, ?)",
        (nom, adresse, pincode)
    )
    conn.commit()
    conn.close()
    
    return redirect(url_for("home"))

@app.route("/students", methods=["GET"])
@token_required
def get_students():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT nom, adresse, pincode FROM students")
    students = c.fetchall()
    conn.close()
    return jsonify(students)
