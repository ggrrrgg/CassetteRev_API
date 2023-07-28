from flask import Blueprint, request
from init import db
from models.user import User
from models.release import Release
from models.review import Review
from models.comment import Comment, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

comment_bp = Blueprint('comment', __name__)

def current_user_is_admin():
    # Assuming you have implemented the 'User' model, and you have access to the current user object.
    # If not, you need to retrieve the current user from your authentication system.
    current_user = User.query.get(get_jwt_identity())
    if current_user and current_user.is_admin:
        return True
    return False


@comment_bp.route('/<int:comment_id>', methods=['GET'])
def get_one_comment(release_id, review_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        return comment_schema.dump(comment)
    else:
        return {'error': f'Comment with id {release_id, review_id, comment_id} not found'}, 404
# /cards/card_id/comments - POST

@comment_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(release_id, review_id):
    body_data = request.get_json()
    stmt = db.select(Review).filter_by(id=review_id) # select * from cards where id=card_id
    review = db.session.scalar(stmt)
    if review:
        comment = Comment(
            comment_txt=body_data.get('comment_txt'),
            user_id=get_jwt_identity(), # pass id to the _id field
            reviews=review # pass the model instance to the model field
        )

        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    else:
        return {'error': f'Review not found with id {release_id, review_id}'}, 404

@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(release_id, review_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    if current_user_is_admin():
        # Admins are granted permission to delete any release
        db.session.delete(comment)
        db.session.commit()
        return {'message': f'Comment {release_id, review_id, comment_id} deleted successfully'}
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'message': f'Comment {release_id, review_id, comment_id} deleted successfully'}
    else:
        return {'error': f'Comment not found with id {release_id, review_id, comment_id}'}, 404
    
@comment_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(release_id, review_id, comment_id):
    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt) # comment from database that needs to be updated
    if comment:
        comment.comment_txt = body_data.get('comment_txt') or comment.comment_txt
        db.session.commit()
        return comment_schema.dump(comment)
    else:
        return {'error': f'Comment {release_id, review_id, comment_id} not found'}, 404