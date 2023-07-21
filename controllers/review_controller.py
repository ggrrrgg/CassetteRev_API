from flask import Blueprint, request
from init import db
from models.user import User
from models.review import Review, review_schema, reviews_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

reviews_bp = Blueprint('reviews', __name__)


# @reviews_bp.route('/', methods=['GET'])
# def get_all_reviews():
#     stmt = db.select(Review)
#     reviews = db.session.scalars(stmt)
#     return reviews_schema.dump(reviews)

# @reviews_bp.route('/<int:id>')
# def get_one_review(id):
#     stmt = db.select(Review).filter_by(id=id)
#     review = db.session.scalar(stmt)
#     if review:
#         return review_schema.dump(review)
#     else:
#         return {'error': f'Release not found with id {id}'}, 404
    

@reviews_bp.route('/', methods=['POST'])
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