from flask import Flask, jsonify
import os
from extensions import db
from routes.tasks import tasks_bp  # Auth removed since login is ignored

def create_app():
    """Factory to create and configure the Flask app."""
    app = Flask(__name__)

    # --- Configurations ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecretkey')

    # Use Render writable directory for SQLite
    db_path = os.path.join("/tmp", "site.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f"sqlite:///{db_path}")
    app.config['UPLOAD_FOLDER'] = 'uploads'

    # --- Initialize extensions ---
    db.init_app(app)

    # --- Automatically create tables ---
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")

    # --- Register blueprints ---
    app.register_blueprint(tasks_bp)  # Only tasks, auth removed

    # --- Home route ---
    @app.route('/')
    def home():
        """Simple health check route."""
        return jsonify({'message': 'Backend is running successfully!'})

    return app


# --- Expose app for Gunicorn ---
app = create_app()

if __name__ == "__main__":
    # Only for local development (not needed on Render)
    app.run(host="0.0.0.0", port=5000, debug=True)
