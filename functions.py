from models.user import User
from flask_jwt_extended import get_jwt_identity

# function to check if current user is admin
def current_user_is_admin():
    # get token from current session user
    current_user = User.query.get(get_jwt_identity())
    # check if is_admin=True
    if current_user and current_user.is_admin:
        return True
    return False