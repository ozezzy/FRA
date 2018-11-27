# instantiate db and seed a user

from model import db, User, hash_password


def seed():
    db.create_all()
    user = User(username='admin', password=hash_password('password'))
    db.session.add(user)
    db.session.commit()


seed()
