from init import db, ma
from marshmallow import fields

# define Model for Release table 
class Release(db.Model):
    __tablename__ = 'releases'
# release table columns
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    date_released = db.Column(db.Date)
    genre = db.Column(db.String)
# foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# define Flask relationships to reflect foreign keys
    user = db.relationship('User', back_populates='releases')
    reviews = db.relationship('Review', back_populates='releases', cascade='all, delete')

# define marshmallow schema
class ReleaseSchema(ma.Schema):
    user = fields.Nested('ReleaseSchema', only=['user_id', 'email'])
    reviews = fields.Nested('ReviewSchema', only=['user_id', 'rating', 'review_txt'] )
# define fields to return
    class Meta:
        fields = ('id', 'artist', 'title', 'date_released', 'genre', 'reviews', 'user_id')
        ordered = True
# define schema variables 
release_schema = ReleaseSchema()
releases_schema = ReleaseSchema(many=True)
