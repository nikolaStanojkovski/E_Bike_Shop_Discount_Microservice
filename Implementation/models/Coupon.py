from enum import Enum
from app import db


class UserCoupon(db.Model):
    Id = db.Column(db.BigInteger, primary_key=True)
    UserId = db.Column(db.BigInteger, nullable=False)
    Code = db.Column(db.String(15), nullable=False)
    ValidFrom = db.Column(db.DateTime, nullable=False)
    ValidTo = db.Column(db.DateTime, nullable=False)
    Type = db.Column(db.String, nullable=False)
    Amount = db.Column(db.Integer, nullable=False)
