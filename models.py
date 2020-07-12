from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    usrn = db.Column(db.String(100), primary_key=True, unique=True)
    name = db.Column(db.String(500))
    password = db.Column(db.String(100))

    def get_id(self):
        return self.usrn


class BookInfo(UserMixin, db.Model):
    __tablename__ = "bookinfo"
    isbn = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(35))
    author = db.Column(db.String(30))
    year = db.Column(db.Integer)


class Review(UserMixin, db.Model):
    __tablename__ = "reviews"
    title = db.Column(db.String(35), primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(500))
