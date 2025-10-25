# create_tables.py
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try different import patterns based on your app structure
    try:
        from app import app, db
        print("Imported from app.py")
    except ImportError:
        from main import app, db
        print("Imported from main.py")
    except ImportError:
        from run import app, db
        print("Imported from run.py")
    except ImportError:
        # If all else fails, create a minimal app
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework_marketplace.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'your-secret-key-here'
        
        db = SQLAlchemy(app)
        
        # Define User model based on your error
        class User(db.Model):
            __tablename__ = 'user'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True, nullable=False)
            password = db.Column(db.String(120), nullable=False)
            role = db.Column(db.String(20), nullable=False)
            rating = db.Column(db.Float, default=0.0)
            total_tasks = db.Column(db.Integer, default=0)
        
        print("Created new Flask app and User model")

    def create_database_tables():
        with app.app_context():
            db.create_all()
            print("All database tables created successfully!")
            print(f"Database should be at: {os.path.abspath('homework_marketplace.db')}")

    if __name__ == '__main__':
        create_database_tables()

except Exception as e:
    print(f"Error: {e}")
    print("Let's try a different approach...")
    
    # Alternative approach
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    import os
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework_marketplace.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'temp-secret-key'
    
    db = SQLAlchemy(app)
    
    # Define the exact User model that matches your application
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password = db.Column(db.String(120), nullable=False)
        role = db.Column(db.String(20), nullable=False)
        rating = db.Column(db.Float, default=0.0)
        total_tasks = db.Column(db.Integer, default=0)
    
    with app.app_context():
        db.create_all()
        print("Database tables created using alternative method!")
        print(f"Database file: {os.path.abspath('homework_marketplace.db')}")
