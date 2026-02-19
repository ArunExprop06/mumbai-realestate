import os
from flask import Flask, request
from config import Config
from extensions import db, login_manager, migrate, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Exempt API endpoints from CSRF
    from routes.public import public_bp
    from routes.auth import auth_bp
    from routes.agent import agent_bp
    from routes.admin import admin_bp
    from routes.api import api_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # CSRF exemption for AJAX API
    csrf.exempt(public_bp)
    csrf.exempt(api_bp)

    # Context processors
    @app.context_processor
    def inject_globals():
        from helpers import AMENITY_ICONS
        return dict(amenity_icons=AMENITY_ICONS)

    @app.template_global()
    def modify_query(**new_values):
        """Build URL with current query params, overriding specified ones."""
        args = request.args.copy()
        for key, val in new_values.items():
            if val is None or val == '':
                args.pop(key, None)
            else:
                args[key] = val
        return '{}?{}'.format(request.path, '&'.join(f'{k}={v}' for k, v in args.items() if v))

    # Create tables and seed data
    with app.app_context():
        import models  # noqa: F401
        db.create_all()
        from seed import seed_all
        seed_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
