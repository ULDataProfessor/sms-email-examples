from flask_socketio import emit


def broadcast_update(room, data):
    emit('battle_update', data, room=room, namespace='/', broadcast=True)

