from flask import Flask, jsonify
import os

def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV') or 'development'
    app.config.from_object(f'config.{env.capitalize()}Config')

    # Optional: Print configuration values for debugging
    print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
    print(f"SUMSUB_API_URL: {app.config.get('SUMSUB_API_URL')}")
    print(f"SUMSUB_API_TOKEN: {app.config.get('SUMSUB_API_TOKEN')}")

    # Register the blueprint
    from app.routes import routes
    app.register_blueprint(routes)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    # Debug: Print all registered routes
    for rule in app.url_map.iter_rules():
        print(rule)
    
    return app
