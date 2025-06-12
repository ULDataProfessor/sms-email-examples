from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Card, UserCard, Transaction

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/list', methods=['POST'])
@jwt_required()
def list_for_sale():
    # TODO: implement listing of card for sale
    return jsonify({'msg': 'list for sale - TODO'})


@transactions_bp.route('/marketplace', methods=['GET'])
@jwt_required(optional=True)
def view_marketplace():
    # TODO: return marketplace listings
    return jsonify([])


@transactions_bp.route('/buy', methods=['POST'])
@jwt_required()
def buy_card():
    # TODO: implement buying logic
    return jsonify({'msg': 'buy card - TODO'})
