from flask import Flask
import os
from extensions import db
from routes.auth import auth_bp
from routes.tasks import tasks_bp

def create_app():
    app = Flask(__name__)

    # --- Configurations ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecretkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    app.config['UPLOAD_FOLDER'] = 'uploads'

    # --- Initialize extensions ---
    db.init_app(app)

    # --- Automatically create tables ---
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")

    # --- Register blueprints with URL prefixes ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # --- Optional home route ---
    @app.route('/')
    def home():
        return {'message': 'Backend is running successfully!'}

    return app

# --- Expose app for Gunicorn ---
app = create_app()

if __name__ == "__main__":
    # For local development
    app.run(host="0.0.0.0", port=5000, debug=True)
