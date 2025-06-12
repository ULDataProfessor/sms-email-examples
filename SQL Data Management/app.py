from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from config import Config
import os


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": app.config.get('CORS_ORIGINS')}})

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

    os.makedirs(os.path.join(os.path.dirname(__file__), 'data'), exist_ok=True)

    @app.route('/')
    def index():
        return send_from_directory('templates', 'index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
