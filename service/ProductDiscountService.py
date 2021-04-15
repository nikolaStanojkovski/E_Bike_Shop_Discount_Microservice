from datetime import timedelta, datetime

from models.Product import Product
from repository.ProductDiscountRepository import ProductDiscountRepository


class ProductDiscountService:

    def __init__(self):
        self.productDiscountRepository = ProductDiscountRepository()

    # CRUD Functionalities

    def applyDiscountOnProduct(self, productBody):

        foundProduct = self.productDiscountRepository.checkIfProductIsInDatabase(productBody['Id'])
        if foundProduct:
            return self.productDiscountRepository.updateProductDiscount(productBody['Id'], productBody)

        type = productBody['Type']

        ValidFrom = datetime.now()
        ValidTo = datetime.now()

        # Generating the percentage based on the how much was the product sold
        if type == 'mostBought':
            discountPercentage = 10
            ValidTo = ValidFrom + timedelta(days=30)
        elif type == 'leastBought':
            discountPercentage = 20
            ValidTo = ValidFrom + timedelta(days=30)
        else:
            return {'error': 'Type of product discount can only be mostBought or leastBought. {} is illegal type.'.format(type)}, 400

        timesBought = 0
        newProduct = Product(Id=productBody['Id'],
                                TimesBought=timesBought,
                                ValidFrom=ValidFrom,
                                ValidTo=ValidTo,
                                Type=type,
                                DiscountPercentage=discountPercentage)

        return self.productDiscountRepository.applyDiscountOnProduct(newProduct=newProduct)


    def updateProduct(self, productId, productBody):
        return self.productDiscountRepository.updateProductDiscount(productId=productId, productBody=productBody)


    def getAllValidProductDiscounts(self):
        products = self.productDiscountRepository.getAllValidProductDiscounts()
        for_return = []
        for product in products:
            for_return.append(self.productDiscountRepository.getProductById(product.Id))

        return for_return

    def getAllProductDiscounts(self):
        products = self.productDiscountRepository.getAllProductDiscounts()
        for_return = []
        for product in products:
            for_return.append(self.productDiscountRepository.getProductById(product.Id))

        return for_return

    def getProductDiscountById(self, productId):
        return self.productDiscountRepository.getProductById(productId)

    def deleteProduct(self, productId):
        return self.productDiscountRepository.deleteProduct(productId)

    def checkIfProductIsOnDiscountAtTheMoment(self, productId):
        return self.productDiscountRepository.checkIfProductIsOnDiscountAtTheMoment(productId)
