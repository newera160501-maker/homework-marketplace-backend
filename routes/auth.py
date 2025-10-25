from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
#@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data.get('username') or not data.get('password'):
            return jsonify({"error": "Username and password are required"}), 400

        # Check for duplicate username
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
        user = User(username=data['username'], password=hashed_password, role=data.get('role', 'user'))

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data.get('username') or not data.get('password'):
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            return jsonify({
                "message": "Login successful",
                "user_id": user.id,
                "role": user.role
            })
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500#
