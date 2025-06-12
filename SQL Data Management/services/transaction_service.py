from models import db, Transaction, Card, User
from sqlalchemy.orm import joinedload

def create_listing(user_id, card_id, quantity, price):
    tx = Transaction(buyer_id=None, seller_id=user_id, card_id=card_id,
                     quantity=quantity, price_per_card=price)
    db.session.add(tx)
    db.session.commit()
    return tx


def get_marketplace(page=1, size=10, min_price=None, max_price=None, card_name=None):
    query = Transaction.query.filter(Transaction.buyer_id == None)
    if min_price is not None:
        query = query.filter(Transaction.price_per_card >= min_price)
    if max_price is not None:
        query = query.filter(Transaction.price_per_card <= max_price)
    if card_name:
        query = query.join(Card).filter(Card.name.ilike(f"%{card_name}%"))

    query = query.options(joinedload(Transaction.card))
    items = query.order_by(Transaction.timestamp.desc()).paginate(page=page, per_page=size, error_out=False)
    results = [
        {
            'id': t.id,
            'seller': t.seller_id,
            'card': {
                'id': t.card.id,
                'name': t.card.name,
                'image_url': t.card.image_url
            },
            'quantity': t.quantity,
            'price_per_card': t.price_per_card
        }
        for t in items.items
    ]
    return {
        'items': results,
        'total': items.total,
        'page': items.page,
        'pages': items.pages
    }
