from marshmallow import Schema, fields, post_load, ValidationError, validates, validate
import json
from pprint import pprint


class TransactionSystem:
    def __init__(self, data_):
        self.data = data_

    def staff_details(self, id_=None):

        if self.data[0]['S_Id'] is None:

            raise TypeError("Insufficient Data to get Staff details")

        if id_ is None:

            staff_details = {}
            for trans in self.data:

                if trans['S_Id'] not in staff_details:

                    staff_details[trans['S_Id']] = [trans['Quantity'], trans['Total_Price']]
                else:

                    staff_details[trans['S_Id']][0] += trans['Quantity']
                    staff_details[trans['S_Id']][1] += trans['Total_Price']
            return staff_details

        _sales = 0
        _profit = 0
        for trans in self.data:
            if trans['S_Id'] == id_:
                _sales += trans['Quantity']
                _profit += trans['Total_Price']
        return [_sales, _profit]

    def customer_details(self, id_=None):

        if self.data[0]['C_Id'] is None:
            raise TypeError("Insufficient Data to get Customer details")

        if id_ is None:

            customer_details = {}
            for trans in self.data:

                if trans['C_Id'] not in customer_details:

                    customer_details[trans['C_Id']] = [trans['Quantity'], trans['Total_Price']]
                else:

                    customer_details[trans['C_Id']][0] += trans['Quantity']
                    customer_details[trans['C_Id']][1] += trans['Total_Price']
            return customer_details

        _sales = 0
        _profit = 0
        for trans in self.data:
            if trans['C_Id'] == id_:
                _sales += trans['Quantity']
                _profit += trans['Total_Price']
        return [_sales, _profit]

    def branch_details(self, b_id_=None, p_id_=None):

        if self.data[0]['B_Id'] is None:

            raise TypeError("Insufficient Data (Missing Branch ID) to get Branch details")
        elif self.data[0]['Inventory'] is None:

            raise TypeError("Insufficient Data (Missing Inventory Details) to get Branch details")

        if b_id_ is None and p_id_ is None:

            branch_details = {}
            for trans in self.data:

                if trans['B_Id'] not in branch_details:

                    branch_details[trans['B_Id']] = {trans['P_Id']: trans['Inventory']}
                else:

                    branch_details[trans['B_Id']][trans['P_Id']] = trans['Inventory']
            return branch_details

        if b_id_ is None:

            branch_details = {}
            for trans in self.data:

                if trans['B_Id'] not in branch_details and trans['P_Id'] == p_id_:
                    branch_details[trans['B_Id']] = trans['Inventory']

            return branch_details

        if b_id_ is not None and p_id_ is None:

            branch_details = {}
            for trans in self.data:
                if trans['B_Id'] == b_id_:
                    branch_details[trans['P_Id']] = trans['Inventory']
            return branch_details

        for trans in self.data:
            if trans['B_Id'] == b_id_ and trans['P_Id'] == p_id_:
                return trans['Inventory']

    def date_transaction(self):
        if self.data[0]['DateTime'] is None:
            raise TypeError("Insufficient Data (Missing DateTime) to Show Transaction Details")
        pprint(self.data)

    def __str__(self):
        return str(self.data)


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
        updates['S_Id'] = staff_id
        for item in data_:
            item.update(updates)
        return TransactionSystem(data_)


class CustomerSchema(Schema):
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
        updates['C_Id'] = customer_id
        for item in data_:
            item.update(updates)
        return TransactionSystem(data_)


class BranchSchema(Schema):
    P_Id = fields.Integer(validate=validate.Range(100000, 100020), required=True)
    Inventory = fields.Integer(required=True)

    @validates('Inventory')
    def validate_quantity(self, inventory):
        if inventory < 0:
            raise ValidationError('Inventory cannot be less than Zero')

    @post_load(pass_many=True)
    def creating_instance(self, data_, many, **kwargs):
        diff = columns - set(data_[0].keys())
        updates = {keys: None for keys in diff}
        updates['B_Id'] = branch_id
        for item in data_:
            item.update(updates)
        return TransactionSystem(data_)


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

    @post_load(pass_many=True)
    def creating_instance(self, data_, many, **kwargs):
        diff = columns - set(data_[0].keys())
        updates = {keys: None for keys in diff}
        for item in data_:
            item.update(updates)
        return TransactionSystem(data_)


def main():

    global customer_id
    customer_id = 100247
    global staff_id
    staff_id = 100078
    global branch_id
    branch_id = 100004

    global columns
    columns = {"T_Id", "P_Id", "Quantity", "Price_Per_item", "Total_Price", "Inventory",
               "DateTime", "C_Id", "S_Id", "B_Id"}

    with open('staff.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        staff = StaffSchema(many=True).load(data)
        s_details = staff.staff_details(staff_id)
        #print(s_details)
        print("\n---------------------------------------------------------------\n")
        print(f"Total Number of Sales by Staff: {staff_id} is {s_details[0]}")
        print(f"Total Profit by Staff: {staff_id} is {s_details[1]}")
        print("\n---------------------------------------------------------------\n")
    except ValidationError as err:
        pprint(err.messages)

    with open('customer.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        customer = CustomerSchema(many=True).load(data)
        c_details = customer.customer_details(customer_id)
        #print(s_details)
        print(f"Total Number of Products bought by Customer: {customer_id} is {c_details[0]}")
        print(f"Total Profit by Customer: {customer_id} is {c_details[1]}")
        print("\n---------------------------------------------------------------\n")
    except ValidationError as err:
        pprint(err.messages)

    with open('branch.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        branch = BranchSchema(many=True).load(data)
        b_details = branch.branch_details(branch_id)
        print(f"Inventory details for Branch: {branch_id}\n")
        pprint(b_details)
        print("\n---------------------------------------------------------------\n")
    except ValidationError as err:
        pprint(err.messages)

    with open('date.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        date = DateSchema(many=True).load(data)
        print("Transactions Between -> 1/1/2019 12:00 AM and 1/1/2020 12:00 AM\n")
        date.date_transaction()
        print("\n---------------------------------------------------------------\n")
    except ValidationError as err:
        pprint(err.messages)


if __name__ == '__main__':
    main()
