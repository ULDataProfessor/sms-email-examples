from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tokens = db.Column(db.Integer, default=500)
    is_admin = db.Column(db.Boolean, default=False)

    cards = db.relationship('UserCard', backref='user', lazy=True)
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy=True)
    decks = db.relationship('Deck', backref='user', lazy=True)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(255))
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    hp = db.Column(db.Integer)


class UserCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    card = db.relationship('Card', backref='user_cards')


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_per_card = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=False)

    cards = db.relationship('DeckCard', backref='deck', lazy=True)


class DeckCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    card = db.relationship('Card')
