from flask import Blueprint, request
from init import db
from models.user import User
from functions import current_user_is_admin
from models.release import Release
from models.review import Review
from models.comment import Comment, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

# comment route extended from release blueprint
comment_bp = Blueprint('comment', __name__)

# retrieve a single comment from db get method, public
@comment_bp.route('/<int:comment_id>', methods=['GET'])
# pass release, review, and comment id from url 
def get_one_comment(release_id, review_id, comment_id):
    # from comment table match id to comment id
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # if match return to client, error if not
    if comment:
        return comment_schema.dump(comment)
    else:
        return {'error': f'Comment with id {release_id, review_id, comment_id} not found'}, 404

# comment route for user to create a comment on a review
@comment_bp.route('/', methods=['POST'])
# user must be logged in
@jwt_required()
# pass release and review id
def create_comment(release_id, review_id):
    # get json client
    body_data = request.get_json()
    # get review from review table match by id
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        # if matched add comment data to fields
        comment = Comment(
            comment_txt=body_data.get('comment_txt'),
            user_id=get_jwt_identity(), 
            reviews=review 
        )
        # add to session and commit
        db.session.add(comment)
        db.session.commit()
        # return to client
        return comment_schema.dump(comment), 201
    else:
        # if not matched id return not found error
        return {'error': f'Review not found with id {release_id, review_id}'}, 404

# comment route for user to delete their comment
@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
# user must be logged in
@jwt_required()
# pass release, review and comment id
def delete_comment(release_id, review_id, comment_id):
    # get comment from table and match by comment id
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # set jwt id as current user variable
    current_user_id = get_jwt_identity()
    # admin can also delete any comment, so check if user is admin and allow delete if so 
    if current_user_is_admin():
        db.session.delete(comment)
        db.session.commit()
        return {'message': f'Comment {release_id, review_id, comment_id} deleted'}
    # if comment user id matches jwt id allow delete, return error if not
    if comment.user_id != current_user_id:
        return {'error': 'You are not authorised to delete this comment'}, 403
    # then if comment id matches db allow delete
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'message': f' Your comment {release_id, review_id, comment_id} deleted successfully'}
    else:
        return {'error': f'Comment not found with id {release_id, review_id, comment_id}'}, 404
    
# comment route for edit comment
@comment_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
# user must be logged in
@jwt_required()
# pass release, review, and comment id from url
def update_comment(release_id, review_id, comment_id):
    # get client data
    body_data = request.get_json()
    # match comment table id to comment id passed
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    # set jwt id as current user variable
    current_user_id = get_jwt_identity()
    # if comment user id matches jwt id allow edit, return error if not
    if comment.user_id != current_user_id:
        return {'error': 'You are not authorised to edit this comment'}, 403
    # note admins cannot edit user comments, only delete if inappropriate 
    # if comment id matches allow edit of comment text
    if comment:
        comment.comment_txt = body_data.get('comment_txt') or comment.comment_txt
        db.session.commit()
        return comment_schema.dump(comment)
    # if no match return not found error
    else:
        return {'error': f'Comment {release_id, review_id, comment_id} not found'}, 404