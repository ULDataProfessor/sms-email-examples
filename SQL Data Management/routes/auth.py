from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Deck
from schemas import RegisterSchema, LoginSchema
import random

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = RegisterSchema().load(request.get_json() or {})
    username = data['username']
    email = data['email']
    password = data['password']

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'msg': 'User exists'}), 400

    user = User(username=username, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    # TODO: assign random starter deck
    return jsonify({'msg': 'registered'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = LoginSchema().load(request.get_json() or {})
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'msg': 'Bad credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)


@auth_bp.route('/protected')
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify(id=user_id)
