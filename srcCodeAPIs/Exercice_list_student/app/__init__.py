from flask import Flask
from app.models import init_db

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"

init_db()

from app import views, auth
