from flask import Blueprint, request, jsonify
from init import db, bcrypt
from models.user import User, user_schema
from functions import current_user_is_admin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import date, timedelta

# auth route blueprint variable
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# auth route to view a user profile, public
@auth_bp.route('/profile/<int:id>', methods=['GET'])
def get_one_user(id):
    # select from user table filtering by id given in url
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    # if found return to client, if not return error
    if user:
        return user_schema.dump(user)
    else:
        return {'error': f'User with id {id} not found'}, 404

# auth route to sign up new user
@auth_bp.route('/signup', methods=['POST'])
def auth_signup():
# create user unless email address already in db, or not null violation
    try:
        # get data from client
        body_data = request.get_json()
        # Create a new User model instance
        user = User()
        # pass datafrom client to model fields
        user.username = body_data.get('username')
        user.email = body_data.get('email')
        # use datetime to pass current date to sign up date
        user.date = date.today()
        # use bcrypt to hash pw
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the user to the session
        db.session.add(user)
        # Commit user to the database
        db.session.commit()
        # return schema to client
        return user_schema.dump(user), 201
    except IntegrityError as err:
        # return integrity error if email already in db
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address already in use' }, 409
        # return integrity error if any field violates not null
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409

# auth route to login user
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    # get json data rom client
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        # set token expiry to 1 day
        expires_delta = timedelta(hours=24)
        # create token
        token = create_access_token(identity=str(user.id), expires_delta=expires_delta)
        # return to client
        return { 'id': user.id, 'email': user.email, 'token': token, 'is_admin': user.is_admin }
    # if login details incorrect return error
    else:
        return { 'error': 'Invalid email or password' }, 401

# delete route to remove user
@auth_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    # get id 
    user = db.session.query(User).get(id)
    # check if user is admin, allow delete if so
    if current_user_is_admin():
        db.session.delete(user)
        db.session.commit()
        return {'message': f'{user.username} deleted successfully'}
    # if user id matches jwt allow delete, return error if not
    if str(user.id) != get_jwt_identity():
        return {'error': 'You are not authorised to delete this user'}, 403
    else:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'{user.username} deleted successfully'}

# auth edit user profile route
@auth_bp.route('/editprofile/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(id):
    # get json data from client
    body_data = user_schema.load(request.get_json(), partial=True)
    # find user by id in db
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    # check if user is admin
    if current_user_is_admin():
        # if user is admin allow changes, if unchanged fields, allow to be unchanged
        user.username = body_data.get('username') or user.username
        user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8') or user.password
        # admin can make other users admin
        user.is_admin = body_data.get('is_admin') or user.is_admin
        # commit changes
        db.session.commit()
        # return to client
        return user_schema.dump(user) and {'message': f'{user.username} updated successfully'}
    # if user id matches
    if user:
        # if user id matches login token allow, error if not
        if str(user.user_id) != get_jwt_identity():
            return {'error': f'Only {user.username} can edit themselves'}, 403
        # allow username and password to be edited by user
        user.username = body_data.get('username') or user.username
        user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')or user.password
        # commit changes
        db.session.commit()
        return user_schema.dump(user) and {'message': f'{user.username} updated successfully'}
    # return not found error if id not matched
    else:
        return {'error': f'User {id} not found'}, 404
