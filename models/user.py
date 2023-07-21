from init import db, ma
from marshmallow import fields
# from datetime import timedelta

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)

    releases = db.relationship('Release', back_populates='user', cascade='all, delete')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    releases = fields.List(fields.Nested('ReleaseSchema', exclude=['user']))
    reviews = fields.List(fields.Nested('ReviewSchema', exclude=['user']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'date', 'releases', 'reviews', 'comments')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])