# create_tables.py
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db  # Adjust import based on your app structure

def create_database_tables():
    with app.app_context():
        db.create_all()
        print("All database tables created successfully!")

if __name__ == '__main__':
    create_database_tables()