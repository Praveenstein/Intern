"""
Validating for branch
"""

from marshmallow import Schema, fields, post_load, ValidationError, validates, validate
import json
from pprint import pprint


class BranchSchema(Schema):
    P_Id = fields.Integer(validate=validate.Range(100000, 100020), required=True)
    Inventory = fields.Integer(required=True)

    @validates('Inventory')
    def validate_quantity(self, inventory):
        if inventory < 0:
            raise ValidationError('Inventory cannot be less than Zero')


with open('branch.json', 'r') as json_file:
    data = json.load(json_file)


try:
    branch = BranchSchema(many=True).load(data)
    pprint(branch)
except ValidationError as err:
    pprint(err.messages)
