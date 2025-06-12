from flask import Flask, send_from_directory, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from models import db
from config import InstanceConfig
import os


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(InstanceConfig)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": app.config.get('CORS_ORIGINS')}})
    socketio = SocketIO(app, cors_allowed_origins=app.config.get('CORS_ORIGINS'))

    if not app.debug:
        @app.before_request
        def https_redirect():
            if request.headers.get('X-Forwarded-Proto', 'http') != 'https':
                url = request.url.replace('http://', 'https://', 1)
                return jsonify({'error': 'redirecting'}), 301, {'Location': url}

        @app.after_request
        def add_hsts(resp):
            resp.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            return resp

    @app.before_request
    def handle_if_modified():
        if request.method == 'GET' and request.path.startswith('/static/'):
            file_path = os.path.join(app.root_path, request.path.strip('/'))
            if os.path.exists(file_path):
                last_mod = os.path.getmtime(file_path)
                ims = request.headers.get('If-Modified-Since')
                if ims and float(ims) >= last_mod:
                    return '', 304

    from routes.auth import auth_bp
    from routes.cards import cards_bp
    from routes.transactions import transactions_bp
    from routes.messages import messages_bp
    from routes.battles import battles_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cards_bp, url_prefix='/cards')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(battles_bp, url_prefix='/battles')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/docs')
    def docs():
        return send_from_directory('.', 'openapi.yaml')

    os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)

    @socketio.on('join')
    def on_join(data):
        room = data.get('room')
        if room:
            join_room(room)

    @socketio.on('message')
    def handle_message(data):
        room = data.get('room')
        emit('message', data, room=room)

    @app.route('/')
    def index():
        return send_from_directory('templates', 'index.html')

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': str(e), 'code': 400}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({'error': 'unauthorized', 'code': 401}), 401

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'not found', 'code': 404}), 404

    @app.errorhandler(500)
    def internal(e):
        return jsonify({'error': 'server error', 'code': 500}), 500

    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
