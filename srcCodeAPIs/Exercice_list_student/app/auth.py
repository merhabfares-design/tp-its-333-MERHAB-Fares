import jwt
from functools import wraps
from flask import request, jsonify, session, redirect, url_for, render_template
from app import app
import datetime

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin123"

@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        # API request
        data = request.get_json()
        login = data.get("login")
        password = data.get("password")
        
        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            token = jwt.encode({
                'user': 'admin',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.config["SECRET_KEY"], algorithm="HS256")
            return jsonify(token=token)
        return jsonify(message="Unauthorized"), 401
    else:
        # Web form request
        login = request.form.get("login")
        password = request.form.get("password")
        
        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Identifiants incorrects")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify(message="Token manquant"), 403
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify(message="Token invalide"), 403
        return f(*args, **kwargs)
    return decorated
