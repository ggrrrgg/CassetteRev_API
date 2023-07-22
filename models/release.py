from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError


class Release(db.Model):
    __tablename__ = 'releases'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String)
    title = db.Column(db.Text)
    date_released = db.Column(db.Date)
    genre = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='releases')
    reviews = db.relationship('Review', back_populates='releases', cascade='all, delete')


class ReleaseSchema(ma.Schema):
    user = fields.Nested('ReleaseSchema', only=['username', 'email'])
    reviews = fields.Nested('ReviewSchema', only=['username', 'rating', 'review_txt'] )

    class Meta:
        fields = ('id', 'artist', 'title', 'date_released', 'genre', 'reviews')
        ordered = True

release_schema = ReleaseSchema()
releases_schema = ReleaseSchema(many=True)
