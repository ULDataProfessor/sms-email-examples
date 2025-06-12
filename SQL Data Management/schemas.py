from marshmallow import Schema, fields

class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class MessageSchema(Schema):
    recipient_id = fields.Int(required=True)
    body = fields.Str(required=True)

class ListCardSchema(Schema):
    card_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price_per_card = fields.Int(required=True)

class BuySchema(Schema):
    transaction_id = fields.Int(required=True)
