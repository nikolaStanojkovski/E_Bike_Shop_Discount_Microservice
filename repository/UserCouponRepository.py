from app import db
from models.Coupon import UserCoupon
from datetime import datetime
from marshmallow import Schema, fields


# Marshmallow configuration
##########################
##########################

class UserCouponSchema(Schema):
    Id = fields.Number()
    UserId = fields.Number()
    Code = fields.Str()
    ValidFrom = fields.DateTime()
    ValidTo = fields.DateTime()
    Type = fields.Str()
    Amount = fields.Number()


schema = UserCouponSchema()


def result_prettifier(coupon):
    result = dict(Id=coupon.Id, UserId=coupon.UserId, Code=coupon.Code,
                  ValidFrom=coupon.ValidFrom, ValidTo=coupon.ValidTo,
                  Type=coupon.Type, Amount=coupon.Amount)
    return schema.dump(result)


# Repository implementation
##########################
##########################

class UserCouponRepository:

    # CRUD functionalities

    def __init__(self):
        pass

    def Coupon_Add(self, new_coupon):
        db.session.add(new_coupon)
        db.session.commit()
        return self.Coupon_Read(coupon_id=new_coupon.Id)

    def Coupon_Read(self, coupon_id):
        found_coupon = db.session.query(UserCoupon).filter_by(Id=coupon_id).first()
        if found_coupon:
            return result_prettifier(found_coupon)
        else:
            return {'error': 'Coupon with id {} not found'.format(coupon_id)}, 404

    def Coupon_Read_Check(self, coupon_id):
        found_coupon = db.session.query(UserCoupon).filter_by(Id=coupon_id).first()
        if found_coupon:
            return found_coupon
        else:
            return {}

    def Coupon_Read_All(self):
        return db.session.query(UserCoupon)

    def Coupon_Update(self, coupon_id, coupon_body):
        found_coupon = self.Coupon_Read_Check(coupon_id)

        if found_coupon:
            found_coupon.Code = coupon_body['Code']
            found_coupon.Amount = coupon_body['Amount']
            found_coupon.Type = 'CUSTOM LEVEL'

            db.session.commit()

            return self.Coupon_Read(coupon_id=coupon_id)
        else:
            return {'error': 'Coupon with id {} not found'.format(coupon_id)}, 404

    def Coupon_Delete(self, coupon_id):
        found_coupon = self.Coupon_Read_Check(coupon_id)

        if found_coupon:
            db.session.delete(found_coupon)
            db.session.commit()

    def Coupon_Read_User(self, user_id):
        found_coupon = db.session.query(UserCoupon).filter_by(UserId=user_id).first()

        if found_coupon:
            return found_coupon
        else:
            return {}
