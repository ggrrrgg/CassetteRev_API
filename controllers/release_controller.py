from flask import Blueprint, request, jsonify
from init import db
from functions import current_user_is_admin
from models.user import User, user_schema
from models.review import review_schema
from models.comment import comment_schema
from models.release import Release, release_schema
from controllers.review_controller import review_bp
from controllers.comment_controller import comment_bp
from flask_jwt_extended import get_jwt_identity, jwt_required

# create releases blueprint route
releases_bp = Blueprint('releases', __name__, url_prefix='/releases')
# register reviews and comments routes on releases
releases_bp.register_blueprint(review_bp, url_prefix='/<int:release_id>/review')
releases_bp.register_blueprint(comment_bp, url_prefix='/<int:release_id>/<int:review_id>/comment')

# add a new release to the db
@releases_bp.route('/new', methods=['POST'])
# must be logged in
@jwt_required()
def create_release():
    # get client data
    body_data = release_schema.load(request.get_json())
    # check to see if release has already been added by another user, have to check by artist and title as no id for new entry yet
    existing_release = Release.query.filter_by(artist=body_data.get('artist'), title=body_data.get('title')).first()
    # return error message if match
    if existing_release:
        return jsonify({'message': 'Release already exists, would you like to write a review?'}), 409
    # pass data to fields
    release = Release(
        artist=body_data.get('artist'),
        title=body_data.get('title'),
        genre=body_data.get('genre'),
        date_released=body_data.get('date_released'),
        user_id=get_jwt_identity()
        )
    # add and commit
    db.session.add(release)
    db.session.commit()
    # return to client
    return release_schema.dump(release), 201

# view all releases route, public
@releases_bp.route('/', methods=['GET'])
def get_all_releases():
    # get all entries from releases model
    releases = Release.query.all()
    # want to include all associated reviews and comments so create a list to nest
    release_data = []
    # for each release get reviews and put in a list
    for release in releases:
        release_info = release_schema.dump(release)
        release_info['reviews'] = []
        # then the same for all comments on those reviews
        for review in release.reviews:
            review_info = review_schema.dump(review)
            review_info['comments'] = []
            # then for each comment append comments list
            for comment in review.comments:
                comment_info = comment_schema.dump(comment)
                review_info['comments'].append(comment_info)
            # append reviews to reviews list
            release_info['reviews'].append(review_info)
        # and append release to releases list
        release_data.append(release_info)
    # then return to client
    return jsonify(release_data)
    
# view a single release route, public
@releases_bp.route('/<int:id>', methods=['GET'])
# pass release id fro url
def get_one_release(id):
    # get releases from table with matching id
    release = Release.query.get(id)
    # same as above
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
    # if release id does not match, return a not found error
    else:
        return {'error': f'Release not found with id {id}'}, 404

# delete a release route 
@releases_bp.route('/<int:id>', methods=['DELETE'])
# must be logged in
@jwt_required()
# pass release id from url
def delete_one_release(id):
    # get release from table matching id
    release = db.session.query(Release).get(id)
    # only an admin can delete any release so check if user is admin, return error if not 
    if current_user_is_admin():
        db.session.delete(release)
        db.session.commit()
        return {'message': f'{release.title} deleted successfully'}
    else:
        return {'error': 'You are not authorised to delete this release'}, 403

# edit relaase route
@releases_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# must be logged in
@jwt_required()
# pass release id from url
def update_one_release(id):
    # get client data
    body_data = release_schema.load(request.get_json(), partial=True)
    # get release from table by id
    stmt = db.select(Release).filter_by(id=id)
    release = db.session.scalar(stmt)
    # set jwt id as current user variable
    current_user_id = get_jwt_identity()
    # if release user id matches jwt id allow edit, return error if not
     # admin can also edit any release, so check if user is admin and allow edit if so 
    if str(release.user_id) != current_user_id:
        return {'error': 'You are not authorised to edit this review'}, 403
   
    if current_user_is_admin():
        pass
    else:
        return {'message': 'You are not authorised to edit this review'}
    
    # if matches id allow edit
    if release:
        
        release.artist = body_data.get('artist') or release.artist
        release.title = body_data.get('title') or release.title
        release.date_released = body_data.get('date_released') or release.date_released
        release.genre = body_data.get('genre') or release.genre
        
        db.session.commit()
        return release_schema.dump(release)
    else:
        return {'error': f'Release not found with id {id}'}, 404
    

