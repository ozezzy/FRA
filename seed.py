# instantiate db and seed a user

from FRA.models import User
from FRA import db


def seed():
    user = User(username='admin', password=User.hash_password('password'))
    db.create_all()
    db.session.add(user)
    db.session.commit()


seed()
