import os
import requests
from models import db, Card
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def fetch_cards():
    url = 'https://api.pokemontcg.io/v2/cards'
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get('data', [])


def upsert_cards(cards):
    with app.app_context():
        for c in cards:
            card = Card.query.filter_by(api_id=c['id']).first()
            if not card:
                card = Card(api_id=c['id'])
            card.name = c['name']
            card.image_url = c.get('images', {}).get('small')
            attacks = c.get('attacks', [])
            card.attack = attacks[0]['damage'] if attacks else 0
            card.defense = 0  # TODO: derive defense
            card.hp = int(c.get('hp', 0)) if c.get('hp') else 0
            db.session.add(card)
        db.session.commit()


if __name__ == '__main__':
    cards = fetch_cards()
    upsert_cards(cards)
