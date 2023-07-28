from flask import Blueprint, request, jsonify
from init import db
from models.user import User, user_schema
from models.review import review_schema
from models.comment import comment_schema
from models.release import Release, release_schema
from controllers.review_controller import review_bp
from controllers.comment_controller import comment_bp
from flask_jwt_extended import get_jwt_identity, jwt_required

releases_bp = Blueprint('releases', __name__, url_prefix='/releases')
releases_bp.register_blueprint(review_bp, url_prefix='/<int:release_id>/review')
releases_bp.register_blueprint(comment_bp, url_prefix='/<int:release_id>/<int:review_id>/comment')


def current_user_is_admin():
    current_user = User.query.get(get_jwt_identity())
    if current_user and current_user.is_admin:
        return True
    return False
            
        
@releases_bp.route('/new', methods=['POST'])
@jwt_required()
def create_release():
    body_data = release_schema.load(request.get_json())
    existing_release = Release.query.filter_by(artist=body_data.get('artist'), title=body_data.get('title')).first()
    if existing_release:
        return jsonify({'message': 'Release already exists, would you like to write a review?'}), 409
    release = Release(
        artist=body_data.get('artist'),
        title=body_data.get('title'),
        genre=body_data.get('genre'),
        date_released=body_data.get('date_released'),
        user_id=get_jwt_identity()
        )
    db.session.add(release)
    db.session.commit()
    return release_schema.dump(release), 201


@releases_bp.route('/', methods=['GET'])
def get_all_releases():
    releases = Release.query.all()

    release_data = []
    for release in releases:
        release_info = release_schema.dump(release)
        release_info['reviews'] = []
        
        for review in release.reviews:
            review_info = review_schema.dump(review)
            review_info['comments'] = []
            
            for comment in review.comments:
                comment_info = comment_schema.dump(comment)
                review_info['comments'].append(comment_info)

            release_info['reviews'].append(review_info)

        release_data.append(release_info)

    return jsonify(release_data)
    

@releases_bp.route('/<int:id>', methods=['GET'])
def get_one_release(id):
    release = Release.query.get(id)

    if release:
        release_info = release_schema.dump(release)
        release_info['reviews'] = []
        
        for review in release.reviews:
            review_info = review_schema.dump(review)
            review_info['comments'] = []
            
            for comment in review.comments:
                comment_info = comment_schema.dump(comment)
                review_info['comments'].append(comment_info)

            release_info['reviews'].append(review_info)

        return jsonify(release_info)
    else:
        return {'error': f'Release not found with id {id}'}, 404

    
@releases_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_release(id):
    release = db.session.query(Release).get(id)
    if current_user_is_admin():
        db.session.delete(release)
        db.session.commit()
        return {'message': f'{release.title} deleted successfully'}

    if str(release.user_id) != get_jwt_identity():
        return {'error': 'You are not authorised to delete this release'}, 403
    else:
        db.session.delete(release)
        db.session.commit()
        return {'message': f'{release.title} deleted successfully'}


@releases_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_release(id):
    body_data = release_schema.load(request.get_json(), partial=True)
    stmt = db.select(Release).filter_by(id=id)
    release = db.session.scalar(stmt)
    if release:
        if str(release.user_id) != get_jwt_identity():
            return {'error': f'Only {user.username} can edit this release'}, 403
        
        release.artist = body_data.get('artist') or release.artist
        release.title = body_data.get('title') or release.title
        release.date_released = body_data.get('date_released') or release.date_released
        release.genre = body_data.get('genre') or release.genre
        
        db.session.commit()
        return release_schema.dump(release)
    else:
        return {'error': f'Release not found with id {id}'}, 404
    

