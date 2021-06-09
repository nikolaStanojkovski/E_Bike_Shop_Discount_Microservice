from app import db


class Product(db.Model):
    Id = db.Column(db.BigInteger, primary_key=True)
    TimesBought = db.Column(db.Integer, nullable=False)
    ValidFrom = db.Column(db.DateTime, nullable=False)
    ValidTo = db.Column(db.DateTime, nullable=False)
    Type = db.Column(db.String, nullable=False)
    DiscountPercentage = db.Column(db.Integer, nullable=True)