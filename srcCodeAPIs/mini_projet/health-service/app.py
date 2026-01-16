from flask import Flask, request, jsonify
import requests, json, os
import jwt
from functools import wraps
from datetime import datetime, timedelta, timezone

SECRET_KEY = "secret123"

app = Flask(__name__)
DATA_FILE = "data.json"
PERSON_SERVICE_URL = "http://person-service:5001"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def person_exists(person_id):
    r = requests.get(f"{PERSON_SERVICE_URL}/persons/{person_id}")
    return r.status_code == 200

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify(message="Token missing"), 403

        try:
            token = auth_header.split(" ")[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify(message="Token invalid"), 403

        return f(*args, **kwargs)
    return decorated


@app.route("/health/<int:person_id>", methods=["POST"])
@token_required
def add_health(person_id):
    if not person_exists(person_id):
        return jsonify(message="Person not found"), 404

    data = load_data()
    data[str(person_id)] = request.get_json()
    save_data(data)

    return jsonify(message="Health data added")


@app.route("/health/<int:person_id>", methods=["GET"])
@token_required
def get_health(person_id):
    if not person_exists(person_id):
        return jsonify(message="Person not found"), 404

    data = load_data()
    return jsonify(data.get(str(person_id), {}))


# ✅ ROUTE PUT (ICI, AVANT app.run)
@app.route("/health/<int:person_id>", methods=["PUT"])
@token_required
def update_health(person_id):
    if not person_exists(person_id):
        return jsonify(message="Person not found"), 404

    data = load_data()

    if str(person_id) not in data:
        return jsonify(message="Health data not found"), 404

    data[str(person_id)] = request.get_json()
    save_data(data)

    return jsonify(message="Health data updated")

@app.route("/health/<int:person_id>", methods=["DELETE"])
@token_required
def delete_health(person_id):
    # vérifier que la personne existe
    if not person_exists(person_id):
        return jsonify(message="Person not found"), 404

    data = load_data()

    # vérifier qu'il y a des données santé
    if str(person_id) not in data:
        return jsonify(message="Health data not found"), 404

    # supprimer les données
    del data[str(person_id)]
    save_data(data)

    return jsonify(message="Health data deleted")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if data["username"] == "admin" and data["password"] == "admin123":
        token = jwt.encode(
            {
                "user": "admin",
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify(token=token)

    return jsonify(message="Unauthorized"), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
