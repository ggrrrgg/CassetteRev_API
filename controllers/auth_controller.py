from flask import Blueprint, request, jsonify
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from models.release import Release, release_schema, releases_schema
from models.review import Review, review_schema, reviews_schema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import date

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return users_schema.dump(users)

@auth_bp.route('/signup', methods=['POST'])
def auth_signup():
    try:
        body_data = request.get_json()

        # Create a new User model instance from the user info
        user = User()
        user.username = body_data.get('username')
        user.email = body_data.get('email')
        user.date = date.today()
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the user to the session
        db.session.add(user)
        # Commit to add the user to the database
        db.session.commit()
        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address already in use' }, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409


@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id))
        return { 'id': user.id, 'email': user.email, 'token': token, 'is_admin': user.is_admin }
    else:
        return { 'error': 'Invalid email or password' }, 401
    
def current_user_is_admin():
    # Assuming you have implemented the 'User' model, and you have access to the current user object.
    # If not, you need to retrieve the current user from your authentication system.
    current_user = User.query.get(get_jwt_identity())
    if current_user and current_user.is_admin:
        return True
    return False


@auth_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    
    user = db.session.query(User).get(id)

    if current_user_is_admin():
        # Admins are granted permission to delete any release
        db.session.delete(user)
        db.session.commit()
        return {'message': f'{user.username} deleted successfully'}

    # If the user is not an admin, check if they are the owner of the release
    if str(user.id) != get_jwt_identity():
        return {'error': 'You are not authorised to delete this user'}, 403
    else:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'{user.username} deleted successfully'}
    
@auth_bp.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(id):
    body_data = user_schema.load(request.get_json(), partial=True)
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if current_user_is_admin():
        # Admins are granted permission to delete any release
        user.username = body_data.get('username') or user.username
        user.password = body_data.get('password') or user.password
        user.is_admin = body_data.get('is_admin') or user.is_admin
        return {'message': f'{user.username} updated successfully'}
    if user:
        if str(user.user_id) != get_jwt_identity():
            return {'error': f'Only {user.username} can edit themselves'}, 403
        user.username = body_data.get('username') or user.username
        user.password = body_data.get('password') or user.password
        
        db.session.commit()
        return user_schema.dump(user)
    else:
        return {'error': f'User {id} not found'}, 404



@auth_bp.route('/release', methods=['POST'])
@jwt_required()
def create_release():
    body_data = release_schema.load(request.get_json())
    # create a new Card model instance
    release = Release(
        artist=body_data.get('artist'),
        title=body_data.get('title'),
        genre=body_data.get('genre'),
        date_released=body_data.get('date_released'),
        user_id=get_jwt_identity()
        
    )
    # Add that card to the session
    db.session.add(release)
    # Commit
    db.session.commit()
    # Respond to the client
    return release_schema.dump(release), 201
    
