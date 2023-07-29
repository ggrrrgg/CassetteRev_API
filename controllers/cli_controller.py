from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.release import Release
from models.review import Review
from models.comment import Comment

db_commands = Blueprint('db', __name__)

# cli create db command
@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")

#  cli delete tables command
@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

# cli seed all tables
@db_commands.cli.command('seed')
def seed_db():
    users = [
        # seed admin user
        User(
            username='Admin',
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        # seed a test standard user
        User(
            username='Dummy1',
            email='dumdum1@email.com',
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]
    # add users
    db.session.add_all(users)
    # seed test releases
    releases = [
        Release(
            artist='de la soul',
            title='stakes is high',
            date_released='2/7/96',
            genre='Hip Hop',
            user=users[0]
        ),
        Release(
            artist='low flung',
            title='microscope impressions',
            date_released='11/2/21',
            genre='Ambient',
            user=users[0]
        )
    ]
    # add releases
    db.session.add_all(releases)
    # seed test reviews
    reviews = [
        Review(
            rating='9',
            review_txt='Next level chef, lets go baby!',
            user=users[1],
            releases=releases[0]
        ),
        Review(
            rating='7',
            review_txt='NGL, its nice',
            user=users[0],
            releases=releases[1]
        )
    ]
    # add reviews
    db.session.add_all(reviews)
    # seed test comments
    comments = [
        Comment(
            comment_txt="Right???",
            user=users[1],
            reviews=reviews[0]
        ),
        Comment(
            comment_txt="Wowee",
            user=users[1],
            reviews=reviews[1]
        )
    ]
    # add comments
    db.session.add_all(comments)
    # commit all to db
    db.session.commit()
    print("Tables seeded")