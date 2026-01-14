# Copilot Instructions for upec-its-333

## Project Overview
This is a course repository for ITS 333, teaching API development with Flask. It contains:
- Two API examples: simple webApi (`myFirstAPI_with_webAPI`) and MVC-structured API (`mySecondAPI_with_MVC`)
- Semi-structured data examples (`srcCodeFichiersSemiStruct`) with GeoJSON
- Exercise templates with `### EXO#` comments indicating incomplete implementations

## Architecture Patterns
- **Simple API**: Single `app.py` with routes defined directly
- **MVC API**: Modular structure with `app/__init__.py` for Flask app creation, `app/views.py` for routes, `app/templates/` for Jinja2 templates
- Data handling: JSON responses via `jsonify()`, GeoJSON for spatial data in `BDD101/data.json`

## Development Workflow
- Run simple API: `python app.py` (from `myFirstAPI_with_webAPI/`)
- Run MVC API: `python run.py` (from `mySecondAPI_with_MVC/`)
- Both use `debug=True` for development
- Install dependencies: `pip install -r requirements.txt` (Flask==3.1.0)

## Coding Conventions
- Flask app initialization: `app = Flask(__name__)` in `__init__.py` or directly in `app.py`
- Route definitions: `@app.route("/api/endpoint", methods=["GET"])` with `jsonify()` returns
- Import pattern: `from app import app` in views, circular import avoided by importing views at end of `__init__.py`
- Exercise placeholders: Use `### EXO# - description` comments for incomplete code sections

## Key Files
- `srcCodeAPIs/myFirstAPI_with_webAPI/app.py`: Example of monolithic API structure
- `srcCodeAPIs/mySecondAPI_with_MVC/app/views.py`: MVC views with route handlers
- `srcCodeFichiersSemiStruct/BDD101/data.json`: GeoJSON FeatureCollection format for spatial data

## Common Patterns
- API responses: `return jsonify(message="text")` or `return jsonify(data=dict)`
- Request handling: `data = request.get_json()` for POST bodies
- Template rendering: `render_template("index.html")` (though templates may be empty in exercises)