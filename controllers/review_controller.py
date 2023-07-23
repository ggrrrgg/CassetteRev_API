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

# @auth_bp.route('/review', methods=['POST'])
# @jwt_required()
# def create_review():
#     body_data = review_schema.load(request.get_json())
#     # create a new Card model instance
#     review = Review(
#         rating=body_data.get('rating'),
#         review_txt=body_data.get('review_txt'),
#         date=date.today(),
#         user_id=get_jwt_identity,
#         release_id=body_data.get('release_id')
#     )
#     # Add that card to the session
#     db.session.add(review)
#     # Commit
#     db.session.commit()
#     # Respond to the client
#     return review_schema.dump(review), 201

