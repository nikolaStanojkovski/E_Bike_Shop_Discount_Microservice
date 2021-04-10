from datetime import datetime, timedelta
import random
import string
from models.Discount import RentingDiscount, BuyingDiscount, ParkingDiscount, DiscountRank
from repository.DiscountRepository import RentingDiscountRepository, BuyingDiscountRepository, ParkingDiscountRepository


class ParkingDiscountService:

    def __init__(self):
        self.parking_discount_repository = ParkingDiscountRepository()

    def read_parking_discount_by_user(self, user_id):
        discount = self.parking_discount_repository.parking_discount_find_by_userId(user_id=user_id)
        if discount:
            return discount
        else:
            return {}

    def parking_discount_add(self, parking_discount_body):
        parking_discount_by_user = self.read_parking_discount_by_user(parking_discount_body['userId'])
        if parking_discount_by_user:
            return {'error': 'User with id {} already has a renting discount'.format(parking_discount_body['userId'])}

        valid_from = datetime.now()
        valid_until = datetime.now()
        percent = 0.0

        letters = string.ascii_lowercase
        generated_code = ''.join(random.choice(letters) for i in range(15))  # Generating random string

        if parking_discount_body['discountRank_type'] == "BronzeParkingMedal":
            percent = 0.1
            valid_until = valid_until + timedelta(weeks=1)
        elif parking_discount_body['discountRank_type'] == "SilverParkingMedal":
            percent = 0.2
            valid_until = valid_until + timedelta(weeks=2)
        elif parking_discount_body['discountRank_type'] == "GoldParkingMedal":
            valid_until = valid_until + timedelta(weeks=3)
            percent = 0.3
        elif parking_discount_body['discountRank_type'] == "Top10Monthly":
            percent = 0.4
            valid_until = valid_until + timedelta(weeks=8)
        elif parking_discount_body['discountRank_type'] == "Top3Annually":
            percent = 0.5
            valid_until = valid_until + timedelta(days=133)

        new_parking_discount = ParkingDiscount(
            userId=parking_discount_body['userId'],
            code=generated_code,
            discountPercent=percent,
            discountRank_type=parking_discount_body['discountRank_type'],
            validFrom=valid_from,
            validUntil=valid_until
        )

        return self.parking_discount_repository.parking_discount_add(new_parking_discount)

    def parking_discount_update(self, parking_discount_id, parking_discount_body):
        return self.parking_discount_repository.parking_discount_update(parking_discount_id, parking_discount_body)

    def parking_discount_read_by_id(self, parking_discount_id):
        return self.parking_discount_repository.parking_discount_find_by_id(parking_discount_id)

    def parking_discount_delete(self, parking_discount_id):
        return self.parking_discount_repository.parking_discount_delete(parking_discount_id)

    def parking_discount_find_all(self):
        data = self.parking_discount_repository.parking_discount_findAll()
        result = []
        for d in data:
            result.append(self.parking_discount_repository.parking_discount_find_by_id(d.id))
        return result


class BuyingDiscountService:

    def __init__(self):
        self.buying_discount_repository = BuyingDiscountRepository()

    def read_buying_discount_by_user(self, user_id):
        discount = self.buying_discount_repository.buying_discount_find_by_userId(user_id=user_id)
        if discount:
            return discount
        else:
            return {}

    def buying_discount_add(self, buying_discount_body):
        buying_discount_by_user = self.read_buying_discount_by_user(buying_discount_body['userId'])
        if buying_discount_by_user:
            return {'error': 'User with id {} already has a buying discount'.format(buying_discount_body['userId'])}

        valid_from = datetime.now()
        valid_until = datetime.now()
        percent = 0.0

        letters = string.ascii_lowercase
        generated_code = ''.join(random.choice(letters) for i in range(15))  # Generating random string

        if buying_discount_body['discountRank_type'] == "BronzeBuyingMedal":
            percent = 0.1
            valid_until = valid_until + timedelta(days=90)
        elif buying_discount_body['discountRank_type'] == "SilverBuyingMedal":
            percent = 0.2
            valid_until = valid_until + timedelta(days=120)
        elif buying_discount_body['discountRank_type'] == "GoldBuyingMedal":
            valid_until = valid_until + timedelta(days=150)
            percent = 0.3
        elif buying_discount_body['discountRank_type'] == "Top10Monthly":
            percent = 0.4
            valid_until = valid_until + timedelta(days=60)
        elif buying_discount_body['discountRank_type'] == "Top3Annually":
            percent = 0.5
            valid_until = valid_until + timedelta(days=365)

        new_buying_discount = BuyingDiscount(
            userId=buying_discount_body['userId'],
            code=generated_code,
            discountPercent=percent,
            discountRank_type=buying_discount_body['discountRank_type'],
            validFrom=valid_from,
            validUntil=valid_until
        )

        return self.buying_discount_repository.buying_discount_add(new_buying_discount)

    def buying_discount_update(self, buying_discount_id, buying_discount_body):
        return self.buying_discount_repository.buying_discount_update(buying_discount_id, buying_discount_body)

    def buying_discount_read_by_id(self, buying_discount_id):
        return self.buying_discount_repository.find_buying_discount_by_id(buying_discount_id)

    def buying_discount_delete(self, buying_discount_id):
        return self.buying_discount_repository.buying_discount_delete(buying_discount_id)

    def buying_discount_find_all(self):
        data = self.buying_discount_repository.buying_discount_findAll()
        result = []
        for d in data:
            result.append(self.buying_discount_repository.find_buying_discount_by_id(d.id))
        return result


class RentingDiscountService:

    def __init__(self):
        self.renting_discount_repository = RentingDiscountRepository()

    def read_renting_discount_by_user(self, user_id):
        renting_discount = self.renting_discount_repository.renting_discount_find_by_userId(user_id=user_id)
        if renting_discount:
            return renting_discount
        else:
            return {}

    def renting_discount_add(self, renting_discount_body):
        renting_discount_by_user = self.read_renting_discount_by_user(renting_discount_body['userId'])
        if renting_discount_by_user:
            return {'error': 'User with id {} already has a renting discount'.format(renting_discount_body['userId'])}

        valid_from = datetime.now()
        valid_until = datetime.now()
        percent = 0.0

        letters = string.ascii_lowercase
        generated_code = ''.join(random.choice(letters) for i in range(15))  # Generating random string

        if renting_discount_body['discountRank_type'] == "BronzeRentingMedal":
            percent = 0.1
            valid_until = valid_until + timedelta(days=30)
        elif renting_discount_body['discountRank_type'] == "SilverRentingMedal":
            percent = 0.2
            valid_until = valid_until + timedelta(days=60)
        elif renting_discount_body['discountRank_type'] == "GoldRentingMedal":
            valid_until = valid_until + timedelta(days=90)
            percent = 0.3
        elif renting_discount_body['discountRank_type'] == "Top10Monthly":
            percent = 0.4
            valid_until = valid_until + timedelta(days=30)
        elif renting_discount_body['discountRank_type'] == "Top3Annually":
            percent = 0.5
            valid_until = valid_until + timedelta(days=60)

        new_renting_discount = RentingDiscount(
            userId=renting_discount_body['userId'],
            code=generated_code,
            discountPercent=percent,
            discountRank_type=renting_discount_body['discountRank_type'],
            validFrom=valid_from,
            validUntil=valid_until
        )

        return self.renting_discount_repository.renting_discount_add(new_renting_discount)

    def renting_discount_update(self, renting_discount_id, renting_discount_body):
        return self.renting_discount_repository.renting_discount_update(renting_discount_id, renting_discount_body)

    def renting_discount_read_by_id(self, renting_discount_id):
        return self.renting_discount_repository.renting_discount_by_id(renting_discount_id)

    def renting_discount_delete(self, renting_discount_id):
        return self.renting_discount_repository.renting_discount_delete(renting_discount_id)

    def renting_discount_find_all(self):
        data = self.renting_discount_repository.renting_discount_findAll()
        result = []
        for d in data:
            result.append(self.renting_discount_repository.renting_discount_by_id(d.id))
        return result
