from flask import Blueprint, jsonify
from models import Card
from services.card_service import get_card
from scripts.import_cards import fetch_cards, upsert_cards

cards_bp = Blueprint('cards', __name__)


@cards_bp.route('/import', methods=['POST'])
def import_cards():
    cards = fetch_cards()
    upsert_cards(cards)
    return jsonify({'msg': 'cards imported'})


@cards_bp.route('/', methods=['GET'])
def list_cards():
    cards = Card.query.all()
    data = [{'id': c.id, 'name': c.name, 'image_url': c.image_url} for c in cards]
    return jsonify(data)


@cards_bp.route('/<int:card_id>', methods=['GET'])
def card_detail(card_id):
    card = get_card(card_id)
    if not card:
        return jsonify({'msg': 'not found'}), 404
    return jsonify(card)
