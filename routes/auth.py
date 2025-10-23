from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    hashed_password = generate_password_hash(
        data['password'], method='pbkdf2:sha256', salt_length=16
    )

    # Default role = 'user' if not provided
    user = User(
        username=data['username'],
        password=hashed_password,
        role=data.get('role', 'user')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "role": user.role
        })

    return jsonify({"message": "Invalid credentials"}), 401
