from flask import Blueprint, request
from init import db
from models.user import User
from models.release import Release, release_schema, releases_schema
from models.review import Review, review_schema, reviews_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

review_bp = Blueprint('review', __name__)

@review_bp.route('/', methods=['POST'])
@jwt_required()
def create_review(release_id):
    body_data = request.get_json()
    stmt = db.select(Release).filter_by(id=release_id) # select * from cards where id=card_id
    release = db.session.scalar(stmt)
    if release:
        review = Review(
            rating=body_data.get('rating'),
            review_txt=body_data.get('review_txt'),
            user_id=get_jwt_identity(), # pass id to the _id field
            releases=release # pass the model instance to the model field
        )

        db.session.add(review)
        db.session.commit()
        return review_schema.dump(review), 201
    else:
        return {'error': f'Release not found with id {release_id}'}, 404

@review_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_one_review(release_id, review_id):
    
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review {release_id, review_id} deleted successfully'}
    else:
        return {'error': f'Review not found'}, 404

@review_bp.route('/<int:review_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_review(release_id, review_id):
    body_data = review_schema.load(request.get_json(), partial=True)
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        if str(review.user_id) != get_jwt_identity():
            return {'error': f'Only {user.username} can edit this release'}, 403
        review.rating = body_data.get('rating') or review.rating
        review.review_txt = body_data.get('review_txt') or review.review_txt
        
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {'error': f'Review {release_id, review_id} not found'}, 404

