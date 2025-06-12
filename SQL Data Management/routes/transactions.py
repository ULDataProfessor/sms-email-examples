from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Card, UserCard, Transaction
from schemas import ListCardSchema, BuySchema
from services.transaction_service import create_listing, get_marketplace

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/list', methods=['POST'])
@jwt_required()
def list_for_sale():
    user_id = get_jwt_identity()
    data = ListCardSchema().load(request.get_json() or {})
    user_card = UserCard.query.filter_by(user_id=user_id, card_id=data['card_id']).first()
    if not user_card or user_card.quantity < data['quantity']:
        return jsonify({'msg': 'insufficient cards'}), 400
    create_listing(user_id, data['card_id'], data['quantity'], data['price_per_card'])
    return jsonify({'msg': 'listed'})


@transactions_bp.route('/marketplace', methods=['GET'])
@jwt_required(optional=True)
def view_marketplace():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    card_name = request.args.get('card_name')
    data = get_marketplace(page, size, min_price, max_price, card_name)
    return jsonify(data)


@transactions_bp.route('/buy', methods=['POST'])
@jwt_required()
def buy_card():
    user_id = get_jwt_identity()
    data = BuySchema().load(request.get_json() or {})
    tx = Transaction.query.get(data['transaction_id'])
    if not tx or tx.buyer_id is not None:
        return jsonify({'msg': 'invalid transaction'}), 400
    tx.buyer_id = user_id
    db.session.commit()
    return jsonify({'msg': 'purchased'})
