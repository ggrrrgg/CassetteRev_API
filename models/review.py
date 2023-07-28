from init import db, ma
from marshmallow import fields

# define Model for Review table 
class Review(db.Model):
    __tablename__ = 'reviews'
# review table columns
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review_txt = db.Column(db.Text)
# foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), nullable=False)
# define Flask relationships to reflect foreign keys
    user = db.relationship('User', back_populates='reviews') 
    releases = db.relationship('Release', back_populates='reviews')
    comments = db.relationship('Comment', back_populates='reviews', cascade='all, delete')

# define marshmallow schema
class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['user_id', 'email'])
    releases = fields.Nested('ReleaseSchema', exclude=['reviews'])
# define fields to return
    class Meta:
        fields = ('id', 'rating', 'review_txt', 'release_id', 'user_id')
        ordered = True
# define schema variables 
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)