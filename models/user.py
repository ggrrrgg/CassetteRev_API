from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False)

    releases = db.relationship('Release', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    releases = fields.List(fields.Nested('ReleaseSchema', exclude=['user']))


    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'date', 'releases', 'comments')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])