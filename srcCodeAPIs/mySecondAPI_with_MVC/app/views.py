from app import app
from flask import Flask, render_template, request, jsonify

print(">>> VIEWS MVC LOADED <<<")

### EXO1 - simple API
@app.route("/api/salutation", methods=["GET"])
def salutation():
    return jsonify(message="Hello World")

### EXO2 - API with simple display
@app.route("/api/utilisateurs", methods=["POST"])
def utilisateurs():
    data = request.get_json()
    nom = data.get("nom")
    return jsonify(message=f"Bonjour {nom}")

### EXO3 - API with parameters display 
@app.route("/api/utilisateurs/<nom>", methods=["GET"])
def utilisateurs_param(nom):
    return jsonify(message=f"Bonjour {nom}")

### EXO4 - API with parameters retrieved from URL 
@app.route("/api/afficher_utilisateur", methods=["GET"])
def afficher_utilisateur():
    nom = request.args.get("nom")
    return jsonify(message=f"Bonjour {nom}")
