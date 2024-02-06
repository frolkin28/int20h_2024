from backend.services.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    password = db.Column(db.String(256))


class Lot(db.Model):
    __tablename__ = 'lots'

    id = db.Column(db.Integer, primary_key=True)
    lot_name = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class Bet(db.Model):
    __tablename__ = 'bets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))
    amount = db.Column(db.Integer)                                     # Якщо використовуєм копійки
    creation_date = db.Column(db.DateTime)


class Picture(db.Model):

    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))






