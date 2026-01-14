from flask import request, jsonify
from app import db
from app.models import Student
from app.auth import token_required, ADMIN_LOGIN, ADMIN_PASSWORD, ADMIN_VALIDATION_CODE
import jwt
import datetime
from app import create_app

def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    code = data.get('code')

    if login == ADMIN_LOGIN and password == ADMIN_PASSWORD and code == ADMIN_VALIDATION_CODE:
        token = jwt.encode({
            'user': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, create_app().config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Authentification échouée'}), 401

@token_required
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@token_required
def add_student():
    data = request.get_json()
    new_student = Student(
        nom=data['nom'],
        adresse=data['adresse'],
        pincode=data['pincode']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201