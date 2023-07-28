from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.release import Release
from models.review import Review
from models.comment import Comment

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            username='Admin',
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            username='Dummy1',
            email='dumdum1@email.com',
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    
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

    db.session.add_all(releases)

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

    db.session.add_all(reviews)

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

    db.session.add_all(comments)
    db.session.commit()
    print("Tables seeded")