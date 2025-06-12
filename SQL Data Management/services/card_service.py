import time
from functools import lru_cache
from models import Card

_CACHE = {}
_TTL = 60 * 60 * 12  # 12 hours


def _now():
    return int(time.time())


def get_card(card_id):
    data = _CACHE.get(card_id)
    if data and _now() - data['ts'] < _TTL:
        return data['val']

    card = Card.query.get(card_id)
    if card:
        value = {
            'id': card.id,
            'name': card.name,
            'image_url': card.image_url,
            'attack': card.attack,
            'defense': card.defense,
            'hp': card.hp,
        }
        _CACHE[card_id] = {'ts': _now(), 'val': value}
        return value
    return None


