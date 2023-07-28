from init import db, ma
from marshmallow import fields



class Release(db.Model):
    __tablename__ = 'releases'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    date_released = db.Column(db.Date)
    genre = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='releases')
    reviews = db.relationship('Review', back_populates='releases', cascade='all, delete')


class ReleaseSchema(ma.Schema):
    user = fields.Nested('ReleaseSchema', only=['user_id', 'email'])
    reviews = fields.Nested('ReviewSchema', only=['user_id', 'rating', 'review_txt'] )

    class Meta:
        fields = ('id', 'artist', 'title', 'date_released', 'genre', 'reviews', 'user_id')
        ordered = True

release_schema = ReleaseSchema()
releases_schema = ReleaseSchema(many=True)
