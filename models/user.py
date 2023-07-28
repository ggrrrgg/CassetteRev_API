from init import db, ma
from marshmallow import fields

# define Model for users table
class User(db.Model):
    __tablename__ = 'users'
# users table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)
# define Flask relationships to reflect foreign keys
    releases = db.relationship('Release', back_populates='user', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')

# define marshmallow schema
class UserSchema(ma.Schema):
    releases = fields.List(fields.Nested('ReleaseSchema'))
    reviews = fields.List(fields.Nested('ReviewSchema'))
    comments = fields.List(fields.Nested('CommentSchema'))
# define fields to return
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'date', 'releases', 'reviews', 'comments')
# define schema variables 
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])