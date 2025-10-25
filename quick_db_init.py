# quick_db_init.py
from app import app, db

with app.app_context():
    db.create_all()
    print("Database tables created!")
    print(f"Using database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Unknown')}")
