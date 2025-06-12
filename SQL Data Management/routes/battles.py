from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.battle_service import broadcast_update

battles_bp = Blueprint('battles', __name__)


@battles_bp.route('/duel', methods=['POST'])
@jwt_required()
def duel():
    user_id = get_jwt_identity()
    broadcast_update(f'battle-{user_id}', {'status': 'duel started'})
    return jsonify({'msg': 'duel started'})


@battles_bp.route('/royale', methods=['POST'])
@jwt_required()
def royale():
    user_id = get_jwt_identity()
    broadcast_update('royale', {'status': f'user {user_id} joined'})
    return jsonify({'msg': 'royale started'})
