from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Swagger UI
    SWAGGER_URL = '/apidocs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Student API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Import routes and auth here to avoid circular imports
    from app import routes

    app.add_url_rule('/login', 'login', routes.login, methods=['POST'])
    app.add_url_rule('/students', 'get_students', routes.get_students, methods=['GET'])
    app.add_url_rule('/students', 'add_student', routes.add_student, methods=['POST'])

    return app