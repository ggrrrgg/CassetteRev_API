from flask import Blueprint, request
from init import db
from models.user import User
from models.review import Review, review_schema, reviews_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/review', methods=['POST'])
@jwt_required()
def create_review():
    body_data = review_schema.load(request.get_json())
    # create a new Card model instance
    review = Review(
        rating=body_data.get('rating'),
        review_txt=body_data.get('review_txt'),
        date=date.today(),
        user_id=get_jwt_identity,
        release_id=body_data.get('release_id')
    )
    # Add that card to the session
    db.session.add(review)
    # Commit
    db.session.commit()
    # Respond to the client
    return review_schema.dump(review), 201