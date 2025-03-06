from encodings.utf_8 import encode
import hashlib
import hmac
import json
from ast import Bytes
from hmac import HMAC


class Item:

    def __init__(self, unitPrice: int, units: int, vatPercentage: float, productCode: str, deliveryDate: str) -> None:
        self.unitPrice = unitPrice
        self.units = units
        self.vatPercentage = vatPercentage
        self.productCode = productCode
        self.deliveryDate = deliveryDate


class Customer:

    def __init__(self, email: str) -> None:
        self.email = email


class RedirectUrls:

    def __init__(self, success: str, cancel: str) -> None:
        self.success = success
        self.cancel = cancel


class Body:
    def __init__(self, stamp: str, reference: str, amount: int,
                 currency: str, language: str, items: list[Item], customer: Customer,
                 redirectUrls: RedirectUrls) -> None:
        self.stamp = stamp
        self.reference = reference
        self.amount = amount
        self.currency = currency
        self.language = language
        self.items = items
        self.customer = customer
        self.redirectUrls = redirectUrls

    # create toDictionary() method to customize a converter of object class to dict type
    def toDictionary(self) -> dict:
        items = []
        for item in self.items:
            items.append(item.__dict__)
        return dict({
            "stamp": self.stamp,
            "reference": self.reference,
            "amount": self.amount,
            "currency": self.currency,
            "language": self.language,
            "items": items,
            "customer": self.customer.__dict__,
            "redirectUrls": self.redirectUrls.__dict__
        })


class Crypto:

    # /
    # @param message Raw string
    # @param secret Merchant shared secret
    # @return
    # /
    @staticmethod
    def compute_sha256_hash(message: str, secret: str) -> str:

        # whitespaces that were created during json parsing process must be removed
        hash = hmac.new(secret.encode(), message.encode(), digestmod=hashlib.sha256)
        return hash.hexdigest()

    # /
    # @param secret Merchant shared secret
    # @param headerParams Headers or query string parameters
    # @param body Request body or empty string for GET request
    # @return
    # /
    @staticmethod
    def calculate_hmac(self, secret: str, headerParams: dict, body: str = '') -> str:

        data = []
        for key, value in headerParams.items():
            if key.startswith('checkout-'):
                data.append('{key}:{value}'.format(key=key, value=value))

        data.append(body)
        return self.compute_sha256_hash('\n'.join(data), secret)


secret = "SAIPPUAKAUPPIAS"
headers = dict({
    "checkout-account": "375917",
    "checkout-algorithm": "sha256",
    "checkout-method": "POST",
    "checkout-nonce": "564635208570151",
    "checkout-timestamp": "2018-07-06T10:01:31.904Z"})
stamp = "unique-identifier-for-merchant"
reference = "3759170"
amount = 1525
currency = "EUR"
language = "FI"

unitPrice = 1525
units = 1
vatPercentage = 25.5
productCode = "#1234"
deliveryDate = "2018-09-01"

item = Item(unitPrice, units, vatPercentage, productCode, deliveryDate)
items = {item}
customer = Customer("test.customer@example.com")
redirectUrls = RedirectUrls("https://ecom.example.com/cart/success", "https://ecom.example.com/cart/cancel")

b = Body(stamp, reference, amount, currency, language, items, customer, redirectUrls)

body = json.dumps(b.toDictionary(), separators=(',', ':'))
encData = Crypto.calculate_hmac(Crypto, secret, headers, body)
print("Encrypted data: " + encData)
# result after running the program:
# Encrypted data: 9a4a7735279de4c99268e4566a5526ae887e73e6e58f2918cb2309ccac366129
