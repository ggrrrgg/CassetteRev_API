from init import db, ma
from marshmallow import fields


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, max=10)
    review_txt = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews') 
    release = db.relationship('Release', back_populates='releases')

class ReviewSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username', 'email'])
    release = fields.Nested('ReleaseSchema', exclude=['reviews'])

    class Meta:
        fields = ('id', 'rating', 'release', 'username')
        ordered = True

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)