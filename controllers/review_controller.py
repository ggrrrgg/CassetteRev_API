from flask import Blueprint, request, jsonify
from init import db
from functions import current_user_is_admin
from models.user import User
from models.release import Release
from models.review import Review, review_schema
from models.comment import comment_schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

# review route added to releases route
review_bp = Blueprint('review', __name__)

# route to view one review, public
@review_bp.route('/<int:review_id>', methods=['GET'])
# pass release id and review id from url
def get_one_review(release_id, review_id):
    # get review fom review table matching id
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    # if matched return review including comments made on review
    if review:
        review_info = review_schema.dump(review)
        review_info['comment'] = []
        
        for comment in review.comments:
            comment_info = comment_schema.dump(comment)
            review_info['comment'].append(comment_info)
        
        return jsonify(review_info)
    # if not matched return not found error
    else:
        return {'error': f'Review with id {release_id, review_id} not found'}, 404

# review route for user to create a review
@review_bp.route('/', methods=['POST'])
# user must be logged in
@jwt_required()
# pass release id from url
def create_review(release_id):
    # get json data from client
    body_data = request.get_json()
    # get release data from release table and match by id
    stmt = db.select(Release).filter_by(id=release_id)
    release = db.session.scalar(stmt)
    # Validate the rating value to be between 0 and 10 before passing to db
    rating = int(body_data.get('rating'))
    if not 0 <= rating <= 10:
        return {'error': 'Invalid rating value. Rating must be between 0 and 10'}, 400
    # if release id matches allow review creation
    if release:
        # pass user data to model fields
        review = Review(
            rating=body_data.get('rating'),
            review_txt=body_data.get('review_txt'),
            user_id=get_jwt_identity(),
            releases=release 
        )
        # add and commit
        db.session.add(review)
        db.session.commit()
        # return to client
        return review_schema.dump(review), 201
    # if no release match return not found error
    else:
        return {'error': f'Release not found with id {release_id}'}, 404

# delete review route
@review_bp.route('/<int:review_id>', methods=['DELETE'])
# user must be logged in
@jwt_required()
# pass release and review id from url
def delete_one_review(release_id, review_id):
    # get review from review table via matching id
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    # set jwt id as current user variable
    current_user_id = get_jwt_identity()
    # if review user id matches jwt id allow delete, return error if not
    if review.user_id != current_user_id:
        return {'error': 'You are not authorised to delete this review'}, 403
    # admin can also delete any review, so check if user is admin and allow delete if so 
    if current_user_is_admin():
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Comment {release_id, review_id} deleted successfully'}
    # if auth ok and review id matches, allow delete and commit
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review {release_id, review_id} deleted successfully'}
    # if review id doesnt match return not found error
    else:
        return {'error':'Review not found'}, 404

# edit review route
@review_bp.route('/<int:review_id>', methods=['PUT', 'PATCH'])
# must be logged in
@jwt_required()
# pass release and review id rom url
def update_one_review(release_id, review_id):
    # get json client data
    body_data = review_schema.load(request.get_json(), partial=True)
    # get review from review table by id
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    # set jwt id as current user variable
    current_user_id = get_jwt_identity()
    # if review user id matches jwt id allow edit, return error if not
    if str(review.user_id) != current_user_id:
        return {'error': 'You are not authorised to edit this review'}, 403
    # note admin cannot edit a review, only delete if inappropriate
    # Validate the rating value to be between 0 and 10 before passing to db
    rating = int(body_data.get('rating'))
    if not 0 <= rating <= 10:
        return {'error': 'Invalid rating value. Rating must be between 0 and 10'}, 400
    # if user is owner of review, rating is valid, and review id matches, allow edit
    if review:
        # pass to fields
        review.rating = body_data.get('rating') or review.rating
        review.review_txt = body_data.get('review_txt') or review.review_txt
        # commit and return to client
        db.session.commit()
        return review_schema.dump(review)
    # if release and review id dont match, return not found error
    else:
        return {'error': f'Review {release_id, review_id} not found'}, 404

