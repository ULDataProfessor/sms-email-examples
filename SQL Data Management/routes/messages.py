from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Message
from schemas import MessageSchema
from flask_socketio import emit

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = MessageSchema().load(request.get_json() or {})
    msg = Message(sender_id=user_id, recipient_id=data['recipient_id'], body=data['body'])
    db.session.add(msg)
    db.session.commit()
    emit('message', {
        'from': user_id,
        'body': data['body'],
        'id': msg.id
    }, room=f'user-{data["recipient_id"]}', namespace='/', broadcast=True)
    return jsonify({'msg': 'sent'})


@messages_bp.route('/', methods=['GET'])
@jwt_required()
def inbox():
    user_id = get_jwt_identity()
    messages = Message.query.filter_by(recipient_id=user_id).all()
    data = [{'id': m.id, 'from': m.sender_id, 'body': m.body} for m in messages]
    return jsonify(data)
