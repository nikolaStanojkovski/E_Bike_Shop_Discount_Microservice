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


def result_prettifier(discount):
    result = dict(id=discount.id, userId=discount.userId, code=discount.code,
                  discountPercent=discount.discountPercent,
                  discountRank_type=discount.discountRank_type,
                  validFrom=discount.validFrom,
                  validUntil=discount.validUntil)
    return schema.dump(result)


class BuyingDiscountRepository:

    def find_buying_discount_by_id(self, buying_discount_id):
        discount = db.session.query(BuyingDiscount).filter_by(id=buying_discount_id).first()
        if discount:
            return result_prettifier(discount)
        else:
            return {'error': 'Parking discount with id {} not found'.format(buying_discount_id)}, 404

    def buying_discount_add(self, new_buying_discount):
        db.session.add(new_buying_discount)
        db.session.commit()
        if db.session.query(BuyingDiscount).filter_by(id=new_buying_discount.id).first():
            return result_prettifier(new_buying_discount)
        else:
            return {'error': 'Discount with id {} not found'.format(new_buying_discount.id)}, 404

    def buying_discount_find(self, buying_discount_id):
        discount = db.session.query(BuyingDiscount).filter_by(id=buying_discount_id).first()

        if discount:
            return result_prettifier(discount)
        else:
            return {'error': 'Discount with id {} not found'.format(buying_discount_id)}, 404

    def buying_discount_findAll(self):
        return db.session.query(BuyingDiscount)

    def update_user_medal(self, user_id, user_rank):
        discount = db.session.query(BuyingDiscount).filter_by(userId=user_id).first()
        if discount:
            discount.discountRank_type = user_rank['discountRank_type']

            db.session.commit()
            updated_discount = db.session.query(BuyingDiscount).filter_by(userId=user_id).first()
            if updated_discount:
                return result_prettifier(updated_discount), 200
            else:
                return {'error': 'Discount with user id {} not found'.format(user_id)}, 404
        else:
            return {'error': 'Discount with user id {} not found'.format(user_id)}, 404

    def buying_discount_update(self, buying_discount_id, buying_discount_body):
        discount = db.session.query(BuyingDiscount).filter_by(id=buying_discount_id).first()

        if discount:
            # discount.userId = buying_discount_body['userId']
            discount.code = buying_discount_body['code']
            discount.discountPercent = buying_discount_body['discountPercent']
            discount.discountRank_type = buying_discount_body['discountRank_type']
            valid_from = datetime.strptime(buying_discount_body['validFrom'], '%d/%m/%y %H:%M:%S')
            discount.validFrom = valid_from
            valid_until = datetime.strptime(buying_discount_body['validUntil'], '%d/%m/%y %H:%M:%S')
            discount.validUntil = valid_until

            db.session.commit()

            updated_discount = db.session.query(BuyingDiscount).filter_by(id=buying_discount_id).first()
            if updated_discount:
                return result_prettifier(updated_discount)
            else:
                return {'error': 'Discount with id {} not found'.format(buying_discount_id)}, 404
        else:
            return {'error': 'Discount with id {} not found'.format(buying_discount_id)}, 404

    def buying_discount_delete(self, buying_discount_id):
        discount = db.session.query(BuyingDiscount).filter_by(id=buying_discount_id).first()

        if discount:
            db.session.delete(discount)
            db.session.commit()
            return result_prettifier(discount)
        else:
            return {'error': 'Discount with id {} not found'.format(buying_discount_id)}, 404

    def buying_discount_find_by_userId(self, user_id):
        renting_discount = db.session.query(BuyingDiscount).filter_by(userId=user_id).first()
        if renting_discount:
            return result_prettifier(renting_discount)
        else:
            return {}


class ParkingDiscountRepository:

    def parking_discount_find_by_id(self, parking_discount_id):
        discount = db.session.query(ParkingDiscount).filter_by(id=parking_discount_id).first()
        if discount:
            return result_prettifier(discount)
        else:
            return {'error': 'Parking discount with id {} not found'.format(parking_discount_id)}, 404


    def parking_discount_add(self, new_parking_discount):
        db.session.add(new_parking_discount)
        db.session.commit()
        if db.session.query(ParkingDiscount).filter_by(id=new_parking_discount.id).first():
            return result_prettifier(new_parking_discount)
        else:
            return {'error': 'Discount with id {} not found'.format(new_parking_discount.id)}, 404

    def parking_discount_findAll(self):
        return db.session.query(ParkingDiscount)

    def update_user_medal(self, user_id, user_rank):
        discount = db.session.query(ParkingDiscount).filter_by(userId=user_id).first()
        if discount:
            discount.discountRank_type = user_rank['discountRank_type']

            db.session.commit()
            updated_discount = db.session.query(ParkingDiscount).filter_by(userId=user_id).first()
            if updated_discount:
                return result_prettifier(updated_discount), 200
            else:
                return {'error': 'Discount with user id {} not found'.format(user_id)}, 404
        else:
            return {'error': 'Discount with user id {} not found'.format(user_id)}, 404


    def parking_discount_update(self, parking_discount_id, parking_discount_body):
        discount = db.session.query(ParkingDiscount).filter_by(id=parking_discount_id).first()
        if discount:
            # discount.userId = parking_discount_body['userId']
            discount.code = parking_discount_body['code']
            discount.discountPercent = parking_discount_body['discountPercent']
            discount.discountRank_type = parking_discount_body['discountRank_type']
            valid_from = datetime.strptime(parking_discount_body['validFrom'], '%d/%m/%y %H:%M:%S')
            discount.validFrom = valid_from
            valid_until = datetime.strptime(parking_discount_body['validUntil'], '%d/%m/%y %H:%M:%S')
            discount.validUntil = valid_until

            db.session.commit()
            discount = db.session.query(ParkingDiscount).filter_by(id=parking_discount_id).first()
            if discount:
                return result_prettifier(discount)
            else:
                return {'error': 'Discount with id {} not found'.format(parking_discount_id)}, 404

    def parking_discount_delete(self, parking_discount_id):
        discount = db.session.query(ParkingDiscount).filter_by(id=parking_discount_id).first()
        if discount:
            db.session.delete(discount)
            db.session.commit()
            return  result_prettifier(discount)
        else:
            return {'error': 'Discount with id {} not found'.format(parking_discount_id)}, 404

    def parking_discount_find_by_userId(self, user_id):
        discount = db.session.query(ParkingDiscount).filter_by(userId=user_id).first()
        if discount:
            return result_prettifier(discount)
        else:
            return {}


class RentingDiscountRepository:

    def renting_discount_add(self, new_renting_discount):
        db.session.add(new_renting_discount)
        db.session.commit()
        if db.session.query(RentingDiscount).filter_by(id=new_renting_discount.id).first():
            return result_prettifier(new_renting_discount)
        else:
            return {'error': 'Discount with id {} not found'.format(new_renting_discount.id)}, 404

    def renting_discount_find(self, renting_discount_id):
        discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if discount:
            return result_prettifier(discount)
        else:
            return {'error': 'Discount with id {} not found'.format(renting_discount_id)}, 404

    def renting_discount_findAll(self):
        return db.session.query(RentingDiscount)

    def renting_discount_by_id(self, renting_discount_id):
        discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if discount:
            return result_prettifier(discount)
        else:
            return {'error': 'Renting discount with id {} not found'.format(renting_discount_id)}, 404

    def update_user_medal(self, user_id, user_rank):
        discount = db.session.query(RentingDiscount).filter_by(userId=user_id).first()
        if discount:
            discount.discountRank_type = user_rank['discountRank_type']

            db.session.commit()
            updated_discount = db.session.query(RentingDiscount).filter_by(userId=user_id).first()
            if updated_discount:
                return result_prettifier(updated_discount), 200
            else:
                return {'error': 'Discount with user id {} not found'.format(user_id)}, 404
        else:
            return {'error': 'Discount with user id {} not found'.format(user_id)}, 404

    def renting_discount_update(self, renting_discount_id, renting_discount_body):
        renting_discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if renting_discount:
            # validFrom and validUntil must be in the following pattern : '18/09/19 01:55:19' == 'day/month/year
            # hour:minute:seconds'

            # renting_discount.userId = renting_discount_body['userId']
            renting_discount.code = renting_discount_body['code']
            renting_discount.discountPercent = renting_discount_body['discountPercent']
            renting_discount.discountRank_type = renting_discount_body['discountRank_type']
            valid_from = datetime.strptime(renting_discount_body['validFrom'], '%d/%m/%y %H:%M:%S')
            renting_discount.validFrom = valid_from
            valid_until = datetime.strptime(renting_discount_body['validUntil'], '%d/%m/%y %H:%M:%S')
            renting_discount.validUntil = valid_until

            db.session.commit()

            discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()

            return result_prettifier(discount)
        else:
            return {'error': 'Discount with id {} not found'.format(renting_discount_id)}, 404
    
    def renting_discount_delete(self, renting_discount_id):
        renting_discount = db.session.query(RentingDiscount).filter_by(id=renting_discount_id).first()
        if renting_discount:
            db.session.delete(renting_discount)
            db.session.commit()
            return result_prettifier(renting_discount)
        else:
            return {'error': 'Discount with id {} not found'.format(renting_discount_id)}, 404

    def renting_discount_find_by_userId(self, user_id):
        renting_discount = db.session.query(RentingDiscount).filter_by(userId=user_id).first()
        if renting_discount:
            return result_prettifier(renting_discount)
        else:
            return {}
