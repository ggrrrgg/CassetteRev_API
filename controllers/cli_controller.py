from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.release import Release
# from models.comment import Comment
from datetime import date

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
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            username='Dummy1',
            email='user1@email.com',
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

    db.session.add_all(cards)

    # comments = [
    #     Comment(
    #         message="Comment 1",
    #         user=users[0],
    #         card=cards[0]
    #     ),
    #     Comment(
    #         message="Comment 2",
    #         user=users[1],
    #         card=cards[2]
    #     ),
    #     Comment(
    #         message="Comment 3",
    #         user=users[1],
    #         card=cards[3]
    #     ),
    #     Comment(
    #         message="Comment 4",
    #         user=users[0],
    #         card=cards[3]
    #     )
    # ]

    # db.session.add_all(comments)

    # db.session.commit()


    print("Tables seeded")