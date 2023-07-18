from flask import Blueprint, request
from init import db
from models.user import User
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required


@reviews_bp.route('/')
def get_all_reviews():
    stmt = db.select(Review).order_by(Review.artist.title())
    reviews = db.session.scalars(stmt)
    return reviews_schema.dump(reviews)

@reviews_bp.route('/<int:id>')
def get_one_review(id):
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
        return review_schema.dump(review)
    else:
        return {'error': f'Release not found with id {id}'}, 404
    

# @reviews_bp.route('/', methods=['POST'])
# # @jwt_required()
# def create_review():
#     body_data = review_schema.load(request.get_json())
#     # create a new Card model instance
#     review = Review(
#         title=body_data.get('title'),
#         description=body_data.get('description'),
#         date=date.today(),
#         status=body_data.get('status'),
#         priority=body_data.get('priority'),
#         user_id=get_jwt_identity()
#     )
#     # Add that card to the session
#     db.session.add(card)
#     # Commit
#     db.session.commit()
#     # Respond to the client
#     return card_schema.dump(card), 201