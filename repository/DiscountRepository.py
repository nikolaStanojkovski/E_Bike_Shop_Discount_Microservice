from app import db
from models.Discount import RentingDiscount, BuyingDiscount, ParkingDiscount
from marshmallow import Schema, fields
from datetime import datetime

# JSON Prettifier configuration with Marshmallow


class RentingDiscountSchema(Schema):
    id = fields.Number()
    userId = fields.Number()
    code = fields.Str()
    discountPercent = fields.Float()
    discountRank_type = fields.Str()
    validFrom = fields.DateTime()
    validUntil = fields.DateTime()


schema = RentingDiscountSchema()


class RentingDiscountRepository:

    def result_prettifier(self, discount):
        result = dict(id=discount.id, userId=discount.userId, code=discount.code,
                      discountPercent=discount.discountPercent,
                      discountRank_type=discount.discountRank_type,
                      validFrom=discount.validFrom,
                      validUntil=discount.validUntil)
        return schema.dump(result) 

    def renting_discount_add(self, new_renting_discount):
        db.session.add(new_renting_discount)
        db.session.commit()
        if db.session.query(RentingDiscount).filter_by(id=new_renting_discount.id).first():
            return self.result_prettifier(new_renting_discount)
        else:
            return {'error': 'Discount with id {} not found'.format(new_renting_discount.id)}, 404

    def renting_discount_find(self, renting_discount_id):
        discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if discount:
            # valid_from_string = discount.validFrom.strftime("%m/%d/%Y")
            # valid_to_string = discount.validUntil.strftime("%m/%d/%Y")
            return self.result_prettifier(discount)
        else:
            return {'error': 'Discount with id {} not found'.format(renting_discount_id)}, 404

    def renting_discount_findAll(self):
        return db.session.query(RentingDiscount)

    def renting_discount_by_id(self, renting_discount_id):
        discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if discount:
            return self.result_prettifier(discount)
        else:
            return {'error': 'Renting discount with id {} not found'.format(renting_discount_id)}, 404

    def renting_discount_update(self, renting_discount_id, renting_discount_body):
        renting_discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if renting_discount:
            # validFrom and validUntil must be in the following pattern : '18/09/19 01:55:19' == 'day/month/year
            # hour:minute:seconds'

            renting_discount.userId = renting_discount_body['userId']
            renting_discount.code = renting_discount_body['code']
            renting_discount.discountPercent = renting_discount_body['discountPercent']
            renting_discount.discountRank_type = renting_discount_body['discountRank_type']
            valid_from = datetime.strptime(renting_discount_body['validFrom'], '%d/%m/%y %H:%M:%S')
            renting_discount.validFrom = valid_from
            valid_until = datetime.strptime(renting_discount_body['validUntil'], '%d/%m/%y %H:%M:%S')
            renting_discount.validUntil = valid_until

            db.session.commit()

            discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()

            return self.result_prettifier(discount)
        else:
            return {'error': 'Discount with id {} not found'.format(renting_discount_id)}, 404
    
    def renting_discount_delete(self, renting_discount_id):
        renting_discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if renting_discount:
            db.session.delete(renting_discount)
            db.session.commit()
            return self.result_prettifier(renting_discount)
        else:
            return {'error': 'Discount with id {} not found'.format(renting_discount_id)}, 404

    def renting_discount_find_by_userId(self, user_id):
        renting_discount = db.session.query(RentingDiscount).filter_by(userId=user_id).first()
        if renting_discount:
            return self.result_prettifier(renting_discount)
        else:
            return {}
