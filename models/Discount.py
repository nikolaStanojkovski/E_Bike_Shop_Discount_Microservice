from app import db
import enum


class DiscountRank(enum.Enum):
    BronzeParkingMedal = 1
    SilverParkingMedal = 2
    GoldParkingMedal = 3
    BronzeRentingMedal = 4
    SilverRentingMedal = 5
    GoldRentingMedal = 6
    Top10Monthly = 7
    Top3Annually = 8
    BronzeBuyingMedal = 9
    SilverBuyingMedal = 10
    GoldBuyingMedal = 11


class RentingDiscount(db.Model):
    __tablename__ = 'renting_discount'
    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    userId = db.Column(db.BigInteger, nullable=False)
    code = db.Column(db.String(15), nullable=False)
    discountPercent = db.Column(db.Float, nullable=False)
    discountRank_type = db.Column(db.Enum(DiscountRank), nullable=False)
    validFrom = db.Column(db.DateTime, nullable=False)
    validUntil = db.Column(db.DateTime, nullable=False)


class BuyingDiscount(db.Model):
    __tablename__ = 'buying_discount'
    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    userId = db.Column(db.BigInteger, nullable=False)
    code = db.Column(db.String(15), nullable=False)
    discountPercent = db.Column(db.Float, nullable=False)
    discountRank_type = db.Column(db.Enum(DiscountRank), nullable=False)
    validFrom = db.Column(db.DateTime, nullable=False)
    validUntil = db.Column(db.DateTime, nullable=False)


class ParkingDiscount(db.Model):
    __tablename__ = 'parking_discount'
    id = db.Column(db.BigInteger().with_variant(db.Integer, "sqlite"), primary_key=True)
    userId = db.Column(db.BigInteger, nullable=False)
    code = db.Column(db.String(15), nullable=False)
    discountPercent = db.Column(db.Float, nullable=False)
    discountRank_type = db.Column(db.Enum(DiscountRank), nullable=False)
    validFrom = db.Column(db.DateTime, nullable=False)
    validUntil = db.Column(db.DateTime, nullable=False)