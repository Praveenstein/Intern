"""
Validating for dates
"""

from marshmallow import Schema, fields, post_load, ValidationError, validates, validate
import json
from pprint import pprint


class DateSchema(Schema):
    T_Id = fields.Integer(validate=validate.Range(100000, 999999), required=True)
    P_Id = fields.Integer(validate=validate.Range(100000, 100020), required=True)
    C_Id = fields.Integer(validate=validate.Range(100000, 101000), required=True)
    S_Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    B_Id = fields.Integer(validate=validate.Range(100000, 100010), required=True)
    Quantity = fields.Integer(required=True)
    Price_Per_item = fields.Float(required=True)
    Total_Price = fields.Float(required=True)
    DateTime = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)

    @validates('Quantity')
    def validate_quantity(self, quantity):
        if quantity < 1:
            raise ValidationError('Quantity is Too Low')

    @validates('Price_Per_item')
    def validate_price_per_item(self, price_per_item):
        if price_per_item <= 0:
            raise ValidationError('Price Cannot be Zero or less')

    @validates('Total_Price')
    def validate_total_price(self, total_price):
        if total_price <= 0:
            raise ValidationError('Total Price Cannot be Zero or less')


with open('date.json', 'r') as json_file:
    data = json.load(json_file)


try:
    date = DateSchema(many=True).load(data)
    pprint(date)
except ValidationError as err:
    pprint(err.messages)
