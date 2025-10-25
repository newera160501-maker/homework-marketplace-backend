from flask import Blueprint, request, jsonify
from extensions import db
from models import User  # if you use User model
from werkzeug.security import generate_password_hash, check_password_hash

from backend.models import User


ratings_bp = Blueprint('ratings', __name__)

@ratings_bp.route('/rate_solver', methods=['POST'])
def rate_solver():
    data = request.json
    user = User.query.get(data['solver_id'])
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_rating = data['rating']
    total = user.total_tasks
    user.rating = (user.rating * total + new_rating) / (total + 1)
    user.total_tasks += 1
    db.session.commit()
    return jsonify({"message": "Rating updated", "new_rating": user.rating})