import datetime
import hashlib
import binascii

from FRA import app, db

class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    product_area = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    target_date = db.Column(db.String(50), nullable=False)
    client = db.Column(db.String(30), nullable=False)
    client_priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, default="pending")

    def reorder_priorities(client, priority):
        # fetch features with same and higher priority
        features = db.session.query(Feature).filter(
            Feature.client == client, Feature.client_priority > priority-1).all()
        # increment priorities by 1 to create room
        for ft in features:
            db.session.query(Feature).filter(Feature.id == ft.id).update(
                {"client_priority": ft.client_priority+1}, synchronize_session=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(65), nullable=False)

    def hash_password(password):
        password_and_salt = "cc4a5ce1b3df48aec5d22d1f16b894a0b894eccc%s" % password
        return hashlib.sha256(password_and_salt.encode('utf-8')).hexdigest()
