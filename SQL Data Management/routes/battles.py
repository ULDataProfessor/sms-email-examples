from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

battles_bp = Blueprint('battles', __name__)


@battles_bp.route('/duel', methods=['POST'])
@jwt_required()
def duel():
    # TODO: implement duel logic
    return jsonify({'msg': 'duel - TODO'})


@battles_bp.route('/royale', methods=['POST'])
@jwt_required()
def royale():
    # TODO: implement battle royale logic
    return jsonify({'msg': 'royale - TODO'})
