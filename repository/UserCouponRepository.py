from app import db
from models.Coupon import UserCoupon
from datetime import datetime


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
            ValidFromString = found_coupon.ValidFrom.strftime("%m/%d/%Y")
            ValidToString = found_coupon.ValidTo.strftime("%m/%d/%Y")
            return {'Id': found_coupon.Id, 'UserId': found_coupon.UserId, 'Code': found_coupon.Code,
                    'ValidFrom': ValidFromString, 'ValidTo': ValidToString,
                    'Type': found_coupon.Type, 'Amount': found_coupon.Amount}
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
            found_coupon.UserId = coupon_body['UserId']
            found_coupon.Code = coupon_body['Code']
            found_coupon.Amount = coupon_body['Amount']
            found_coupon.Type = '4'

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
