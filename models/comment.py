from init import db, ma
from marshmallow import fields


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment_txt = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    reviews = db.relationship('Review', back_populates='comments')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['user_id', 'email'])
    review = fields.Nested('ReviewSchema', exclude=['comments'])

    class Meta:
        fields = ('id', 'comment_txt', 'release_id', 'user_id')
        ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)