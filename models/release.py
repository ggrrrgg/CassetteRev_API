from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError


class Release(db.Model):
    __tablename__ = "releases"

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String)
    title = db.Column(db.Text)
    date_released = db.Column(db.Date)
    genre = db.Column(db.String)
    priority = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='releases')
    comments = db.relationship('Comment', back_populates='release', cascade='all, delete')

class ReleaseSchema(ma.Schema):
    pass
