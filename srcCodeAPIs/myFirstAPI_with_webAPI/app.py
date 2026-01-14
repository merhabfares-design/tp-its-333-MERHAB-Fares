from flask import Flask, jsonify, request

app = Flask(_name_)

## EXO1: API GET: renvoyer un helloworld - API end point name: "api/salutation"
@app.route("/api/salutation", methods=["GET"])
def salutation():
    return jsonify(message="Hello World")


## EXO2: API POST: renvoyer un nom fourni en parametre - API end point name: "api/utilisateurs"
@app.route("/api/utilisateurs", methods=["POST"])
def utilisateurs():
    data = request.get_json()
    nom = data.get("nom")
    return jsonify(message=f"Bonjour {nom}")


# to be tested with curl: 
# >> curl -i -X GET http://localhost:5000/api/salutation
# >> curl -i -X POST -H 'Content-Type: application/json' -d '{"nom": "Bob"}' http://localhost:5000/api/utilisateurs

if _name_ == "_main_":
    app.run(debug=True)