from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Card, Transaction, Message, Deck

admin_bp = Blueprint('admin', __name__)


def admin_required(func):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            return jsonify({'msg': 'admin only'}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin_bp.route('/users', methods=['GET'])
@admin_required
def all_users():
    users = User.query.all()
    data = [{'id': u.id, 'username': u.username} for u in users]
    return jsonify(data)

# TODO: add CRUD endpoints for other models
