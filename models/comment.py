from init import db, ma
from marshmallow import fields

# define Model for Comment table 
class Comment(db.Model):
    __tablename__ = 'comments'
# Comment table columns
    id = db.Column(db.Integer, primary_key=True)
    comment_txt = db.Column(db.Text)
# foreign key columns
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
# Define Flask relationships to reflect foreign keys
    user = db.relationship('User', back_populates='comments')
    reviews = db.relationship('Review', back_populates='comments')

# define marshmallow schema
class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['user_id', 'email'])
    review = fields.Nested('ReviewSchema', exclude=['comments'])
# define fields to return
    class Meta:
        fields = ('id', 'comment_txt', 'release_id', 'user_id')
        ordered = True
# define schema variables 
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)