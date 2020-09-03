from marshmallow import Schema, fields, post_load, ValidationError, validates, validate
import json
from pprint import pprint


class TransactionSystem:
    def __init__(self, data):
        self.data = data

    def staff(self):
        pass

    def customer(self):
        pass

    def branch(self):
        pass

    def date(self):
        pass

    def __str__(self):
        return str(self.data)


columns = {"T_Id", "P_Id", "Quantity", "Price_Per_item", "Total_Price", "Inventory", "DateTime", "C_Id", "S_Id", "B_Id"}


class StaffSchema(Schema):
    T_Id = fields.Integer(validate=validate.Range(100000, 999999), required=True)
    P_Id = fields.Integer(validate=validate.Range(100000, 100020), required=True)
    Quantity = fields.Integer(required=True)
    Price_Per_item = fields.Float(required=True)
    Total_Price = fields.Float(required=True)

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

    @post_load(pass_many=True)
    def creating_instance(self, data_, many, **kwargs):
        diff = columns - set(data_[0].keys())
        updates = {keys: None for keys in diff}
        for item in data_:
            item.update(updates)
        return TransactionSystem(data_)


with open('staff.json', 'r') as json_file:
    data_ = json.load(json_file)


try:
    staff = StaffSchema(many=True).load(data_)
    print(staff)
except ValidationError as err:
    pprint(err.messages)
