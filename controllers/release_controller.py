from flask import Blueprint, request
from init import db
from models.user import User
from models.release import Release, release_schema, releases_schema
from controllers.review_controller import review_bp
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

releases_bp = Blueprint('releases', __name__, url_prefix='/releases')
releases_bp.register_blueprint(review_bp, url_prefix='/<int:release_id>/review')
# auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@releases_bp.route('/', methods=['GET'])
def get_all_releases():
    stmt = db.select(Release)
    releases = db.session.scalars(stmt)
    return releases_schema.dump(releases)
    

@releases_bp.route('/<int:id>')
def get_one_release(id):
    stmt = db.select(Release).filter_by(id=id)
    release = db.session.scalar(stmt)
    if release:
        return release_schema.dump(release)
    else:
        return {'error': f'Release not found with id {id}'}, 404
    
@releases_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
# @authorise_as_admin
def delete_one_release(id):
    # is_admin = authorise_as_admin()
    # if not is_admin:
    #     return {'error': 'Not authorised to delete cards'}, 403
    stmt = db.select(Release).filter_by(id=id)
    release = db.session.scalar(stmt)
    if release:
        db.session.delete(release)
        db.session.commit()
        return {'message': f'{release.title} deleted successfully'}
    else:
        return {'error': f'Release not found with id {id}'}, 404

@releases_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_release(id):
    body_data = release_schema.load(request.get_json(), partial=True)
    stmt = db.select(Release).filter_by(id=id)
    release = db.session.scalar(stmt)
    user = db.session.scalar(stmt)
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
    

