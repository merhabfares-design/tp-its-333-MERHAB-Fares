from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "database.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/persons", methods=["POST"])
def create_person():
    data = request.get_json()
    name = data.get("name")

    conn = get_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    c.execute("INSERT INTO persons (name) VALUES (?)", (name,))
    conn.commit()
    person_id = c.lastrowid
    conn.close()

    return jsonify(id=person_id, name=name), 201

@app.route("/persons/<int:person_id>", methods=["GET"])
def get_person(person_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, name FROM persons WHERE id=?", (person_id,))
    row = c.fetchone()
    conn.close()

    if row is None:
        return jsonify(message="Person not found"), 404

    return jsonify(id=row[0], name=row[1])

@app.route("/persons/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM persons WHERE id=?", (person_id,))
    conn.commit()
    deleted = c.rowcount
    conn.close()

    if deleted == 0:
        return jsonify(message="Person not found"), 404

    return jsonify(message="Person deleted")

@app.route("/persons", methods=["GET"])
def get_persons():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, name FROM persons")
    rows = c.fetchall()
    conn.close()

    persons = [{"id": row[0], "name": row[1]} for row in rows]
    return jsonify(persons)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

