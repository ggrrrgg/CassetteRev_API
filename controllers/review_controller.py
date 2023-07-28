from flask import Blueprint, request, jsonify
from init import db
from models.user import User
from models.release import Release
from models.review import Review, review_schema
from models.comment import comment_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

review_bp = Blueprint('review', __name__)

def current_user_is_admin():
    # Assuming you have implemented the 'User' model, and you have access to the current user object.
    # If not, you need to retrieve the current user from your authentication system.
    current_user = User.query.get(get_jwt_identity())
    if current_user and current_user.is_admin:
        return True
    return False

@review_bp.route('/<int:review_id>', methods=['GET'])
def get_one_review(release_id, review_id):

    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)

    if review:
        review_info = review_schema.dump(review)

        # Include reviews for the release
        review_info['comment'] = []
        for comment in review.comments:
            comment_info = comment_schema.dump(comment)

            review_info['comment'].append(comment_info)

        return jsonify(review_info)
    else:
        return {'error': f'Review with id {release_id, review_id} not found'}, 404

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

    if current_user_is_admin():
        # Admins are granted permission to delete any release
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Comment {release_id, review_id} deleted successfully'}
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review {release_id, review_id} deleted successfully'}
    else:
        return {'error':'Review not found'}, 404

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

