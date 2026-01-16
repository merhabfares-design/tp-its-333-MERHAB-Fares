from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "websecret"

PERSON_SERVICE = "http://person-service:5001"
HEALTH_SERVICE = "http://health-service:5002"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        r = requests.post(
            f"{HEALTH_SERVICE}/login",
            json={
                "username": request.form["username"],
                "password": request.form["password"]
            }
        )

        if r.status_code == 200:
            session["token"] = r.json()["token"]
            return redirect("/health")

        return render_template("login.html", error="Login incorrect")

    return render_template("login.html")


@app.route("/health", methods=["GET", "POST"])
def health():
    token = session.get("token")
    if not token:
        return redirect("/")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 🔹 ACTIONS FORMULAIRES
    if request.method == "POST":
        action = request.form["action"]

        if action == "add_person":
            requests.post(
                f"{PERSON_SERVICE}/persons",
                json={"name": request.form["name"]}
            )

        elif action == "add_health":
            person_id = request.form["person_id"]

            requests.post(
                f"{HEALTH_SERVICE}/health/{person_id}",
                json={
                    "poids": request.form["poids"],
                    "taille": request.form["taille"]
                },
                headers=headers
            )

    # 🔹 RÉCUPÉRER PERSONNES
    persons = requests.get(f"{PERSON_SERVICE}/persons").json()

    rows = []

    # 🔹 RÉCUPÉRER DONNÉES SANTÉ
    for p in persons:
        r = requests.get(
            f"{HEALTH_SERVICE}/health/{p['id']}",
            headers=headers
        )

        health = r.json() if r.status_code == 200 else {}

        rows.append({
            "id": p["id"],
            "name": p["name"],
            "poids": health.get("poids", "-"),
            "taille": health.get("taille", "-")
        })

    return render_template("health.html", rows=rows)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
