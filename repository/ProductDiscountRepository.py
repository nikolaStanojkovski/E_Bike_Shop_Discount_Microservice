from datetime import datetime, timedelta

from app import db
from models.Product import Product
from marshmallow import Schema, fields


class ProductDiscountSchema(Schema):
    Id = fields.Number()
    TimesBought = fields.Number()
    ValidFrom = fields.DateTime()
    ValidTo = fields.DateTime()
    Type = fields.Str()
    DiscountPercentage = fields.Number()



schema = ProductDiscountSchema()


def result_prettifier(productDiscount):
    result = dict(Id=productDiscount.Id,
                  TimesBought=productDiscount.TimesBought,
                  ValidFrom=productDiscount.ValidFrom,
                  ValidTo=productDiscount.ValidTo,
                  Type=productDiscount.Type,
                  DiscountPercentage=productDiscount.DiscountPercentage)
    return schema.dump(result)


def simple_result_prettifier(productDiscount):
    result = dict(Id=productDiscount.Id,
                  ValidTo=productDiscount.ValidTo,
                  DiscountPercentage=productDiscount.DiscountPercentage)
    return schema.dump(result)


class ProductDiscountRepository:

    # CRUD functionalities

    def __init__(self):
        pass

    def applyDiscountOnProduct(self, newProduct):
        db.session.add(newProduct)
        db.session.commit()
        return self.getProductById(productId=newProduct.Id)


    def getProductById(self, productId):
        foundProduct = db.session.query(Product).filter_by(Id=productId).first()

        if foundProduct:
            return result_prettifier(foundProduct)
        else:
            return {'error': 'Product with id {} not found'.format(productId)}, 404


    def getEssentialInformationForProductById(self,productId):
        foundProduct = db.session.query(Product).filter_by(Id=productId).first()

        if foundProduct:
            return simple_result_prettifier(foundProduct)
        else:
            return {'error': 'Product with id {} not found'.format(productId)}, 404


    def checkIfProductIsInDatabase(self, productId):
        foundProduct = db.session.query(Product).filter_by(Id=productId).first()
        if foundProduct:
            return foundProduct
        else:
            return {}


    def updateProductDiscount(self, productId, productBody):
        if productId != productBody['Id']:
            return {'error': 'Product id in url and in body are not the same'}, 400

        foundProduct = self.checkIfProductIsInDatabase(productId)
        if foundProduct:
            foundProduct.ValidFrom = datetime.now()
            foundProduct.ValidTo = datetime.now() + timedelta(days=30)
            foundProduct.TimesBought = 0

            type = productBody['Type']
            if type == 'mostBought':
                discountPercentage = 10
            elif type == 'leastBought':
                discountPercentage = 20
            else:
                return {'error': 'Type of product discount can only be mostBought or leastBought. {} is illegal type.'.format(type)}, 400

            foundProduct.DiscountPercentage = discountPercentage
            foundProduct.Type = type
            db.session.commit()

            return {'product update': 'Success. The product with id {} is already in the database and it is updated'.format(productBody['Id'])}
        else:
            return {'error': 'Product with id {} not found'.format(productId)}, 404


    def getAllValidProductDiscounts(self):
        return db.session.query(Product).filter(Product.ValidTo > datetime.now())


    def getAllProductDiscounts(self):
        return db.session.query(Product)

    def deleteProduct(self, productId):
        foundProduct = self.checkIfProductIsInDatabase(productId)

        if foundProduct:
            db.session.delete(foundProduct)
            db.session.commit()
            return {'success': 'Product with id {} was successfully deleted'.format(productId)}, 200
        else:
            return {'error': 'Product with id {} not found'.format(productId)}, 404

    def checkIfProductIsOnDiscountAtTheMoment(self, productId):
        foundProduct = self.checkIfProductIsInDatabase(productId)
        if foundProduct:
            if foundProduct.ValidTo > datetime.now():
                return {'success': 'Product with id {} is on discount until {}'.format(foundProduct.Id, foundProduct.ValidTo)}, 200
            else:
                return {'success': 'Product with id {} is not on discount right now'.format(productId)}, 200

        else:
            return {'success': 'Product with id {} is not on discount right now'.format(productId)}, 200
