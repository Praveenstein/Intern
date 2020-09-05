# -*- coding: utf-8 -*-
""" Querying on Transaction details

This script allows the user to use the json file received from web api
and perform operation to get insights like:

    * Total sale units by a staff
    * Total Profit by a staff
    * Total Number of products bought by a customer
    * Total Profit by a customer
    * Inventory left for a given branch and product
    * Transaction details between two given details

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * marshmallow - lightweight Object serialization and deserialization package
    * json - To deal with Json Files
    * logging - To log Errors
    *pprint - To print some data

This file contains the following Classes:

    * TransactionSystem - This class contains the data received from the web API and has methods to perform operations

    * StaffSchema - This class validates the response from the web api when queried about the staff details
                    and uses this data to create an instance of TransactionSystem.
    * CustomerSchema - This class validates the response from the web api when queried about the Customer details
                    and uses this data to create an instance of TransactionSystem.
    * BranchSchema - This class validates the response from the web api when queried about the Branch details
                    and uses this data to create an instance of TransactionSystem.
    * DateSchema - This class validates the response from the web api when queried about the transactions between
                    two datetime and uses this data to create an instance of TransactionSystem.

"""
# Built-In Packages
import json
from pprint import pprint
import logging
import logging.config
from datetime import datetime

# External Packages
from marshmallow import Schema, fields, post_load, ValidationError, validates, validate

__author__ = 'praveen@gyandata.com'


class Staff:
    def __init__(self, id_, email, branch_):
        self.id = id_
        self.email = email
        self.branch = branch_

    def __str__(self):
        return f"Staff Id: {self.id}, Email: {self.email}, Branch Id: {self.branch.id}"


class Customer:
    def __init__(self, id_, email):
        self.id = id_
        self.email = email

    def __str__(self):
        return f"Customer Id: {self.id}, Email: {self.email}"


class Branch:
    def __init__(self, id_, products_):
        self.id = id_
        self.products = products_

    def __str__(self):
        return f"Branch Id: {self.id}"


class Transaction:
    def __init__(self, id_, staff_, customer_, branch_=None, _datetime=None):
        self.id = id_
        self.staff = staff_
        self.customer = customer_
        self.branch = branch_
        self.datetime = _datetime

    def __str__(self):
        return f"Transaction Id: {self.id}, Handling Staff: {self.staff.id}, " \
               f" Customer: {self.customer.id}, Handling Branch: {self.branch.id}, Date: {self.datetime}"


class Product:
    def __init__(self, id_, price):
        self.id = id_
        self.price = price

    def __str__(self):
        return f"Product Id: {self.id}, Price Per Product: {self.price}"


class Purchase:
    def __init__(self, pu_id_, transaction_, product_, quantity, total_price):
        self.id = pu_id_
        self.transaction = transaction_
        self.product = product_
        self.quantity = quantity
        self.total_price = total_price

    def __str__(self):
        return f"Purchase Id: {self.id}\nTransaction Id: {self.transaction.id}\nProduct: {self.product.id}\n" \
               f"Quantity: {self.quantity}\nTotal Price: {self.total_price}"


class TransactionSystem:
    def __init__(self):
        self.staffs = []
        self.customers = []
        self.branches = []
        self.transactions = []
        self.products = []
        self.purchases = []

    def get_staff(self, id_):
        for _staff in self.staffs:
            if _staff.id == id_:
                return _staff
        raise Exception("Staff Not in DB")

    def get_customer(self, id_):
        for _customer in self.customers:
            if _customer.id == id_:
                return _customer
        raise Exception("customer Not in DB")

    def get_branch(self, id_):
        for _branch in self.branches:
            if _branch.id == id_:
                return _branch
        raise Exception("Branch Not in DB")

    def get_transaction(self, id_):
        for _transaction in self.transactions:
            if _transaction.id == id_:
                return _transaction
        raise Exception("Transaction Not in DB")

    def get_purchase(self, id_):
        for _purchase in self.purchases:
            if _purchase.id == id_:
                return _purchase
        raise Exception("Purchase Not in DB")

    def get_product(self, id_):
        for _product in self.products:
            if _product.id == id_:
                return _product
        raise Exception("Product Not in DB")

    def get_staff_details(self, _id):
        _data = f"The Transactions Handled by Staff: {_id}\n-------------------------------------"
        for _trans in self.transactions:
            if _trans.staff.id == _id:
                _data += f"Transaction Id: {_trans.id}\nCustomer: {_trans.customer.id}\n" \
                         f"Handling Branch: {_trans.branch.id}\nDate: {_trans.datetime}\n" \
                         f"-------------------------------------"
        print(_data)

    def get_customer_details(self, _id):
        _data = f"The Transactions In which the Customer: {_id} was involved:\n-------------------------------------"
        for _trans in self.transactions:
            if _trans.customer.id == _id:
                _data += f"Transaction Id: {_trans.id}\nStaff: {_trans.staff.id}\n" \
                         f"Handling Branch: {_trans.branch.id}\nDate: {_trans.datetime}\n" \
                         f"-------------------------------------"
        print(_data)

    def get_transaction_details(self):
        _data = f"The Transactions Details are\n-------------------------------------"
        for _trans in self.transactions:
            print(f"\nFor the Transaction: {_trans.id}")
            for _purchase in self.purchases:
                if _purchase.transaction.id == _trans.id:
                    print(f"\nPurchase:{_purchase.id}\nProduct: {_purchase.product.id}\nQuantity: {_purchase.quantity}"
                          f"Total Price: {_purchase.total_price}")
            print("\n-------------------------------------")

    def get_staff_performance(self, _id):
        _quantity = 0
        _total_price = 0
        for _trans in self.transactions:
            if _trans.staff.id == _id:
                for _purchase in self.purchases:
                    if _purchase.transaction.id == _trans:
                        _quantity += _purchase.quantity
                        _total_price += _purchase.total_price

        print(f"The Number of Products sold by {_id}: {_quantity} and Total Monetary Value: {_total_price}")

    def get_customer_value(self, _id):
        _quantity = 0
        _total_price = 0
        for _trans in self.transactions:
            if _trans.customer.id == _id:
                for _purchase in self.purchases:
                    if _purchase.transaction.id == _trans:
                        _quantity += _purchase.quantity
                        _total_price += _purchase.total_price

        print(f"The Number of Products Bought by Customer: {_id}: {_quantity} and Total Monetary Value: {_total_price}")

    def get_branch_inventory(self, _id):
        _branch = self.get_branch(_id)
        print(f"\n\nThe Inventory Details for Branch: {_id}\n--------------------------------\n\n")
        for _product in _branch.products:
            print(f"The Inventory for Product: {_product[0].id} is {_product[1]}")


class StaffSchema(Schema):
    Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    Email = fields.Email(required=True)
    B_Id = fields.Integer(validate=validate.Range(100000, 100010), required=True)


class CustomerSchema(Schema):
    Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    Email = fields.Email(required=True)


class BranchSchema(Schema):
    B_Id = fields.Integer(validate=validate.Range(100000, 100010), required=True)
    Pr_Id = fields.Integer(validate=validate.Range(100000, 100021), required=True)
    Inventory = fields.Integer(required=True)

    @validates('Inventory')
    def validate_inventory(self, _inventory):
        if _inventory < 0:
            raise ValidationError('Inventory Cannot Be Negative')


class TransactionSchema(Schema):
    T_Id = fields.Integer(validate=validate.Range(100000, 102000), required=True)
    DateTime = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    C_Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    S_Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    B_Id = fields.Integer(validate=validate.Range(100000, 100010), required=True)


class ProductSchema(Schema):
    Id = fields.Integer(validate=validate.Range(100000, 100021), required=True)
    Price = fields.Float(required=True)

    @validates('Price')
    def validate_price(self, _price):
        if _price <= 0:
            raise ValidationError('Price Cannot be Zero or less')


class PurchaseSchema(Schema):
    P_Id = fields.Integer(validate=validate.Range(100000, 104000), required=True)
    T_Id = fields.Integer(validate=validate.Range(100000, 102000), required=True)
    Pr_Id = fields.Integer(validate=validate.Range(100000, 100021), required=True)
    Quantity = fields.Integer(required=True)
    T_price = fields.Float(required=True)

    @validates('Quantity')
    def validate_quantity(self, _quantity):
        if _quantity <= 0:
            raise ValidationError('Quantity Cannot be Zero or less')

    @validates('T_price')
    def validate_total_price(self, _price):
        if _price <= 0:
            raise ValidationError('Price Cannot be Zero or less')


class TransactionSystemSchema(Schema):
    STAFF = fields.Nested(StaffSchema(many=True))
    CUSTOMERS = fields.Nested(CustomerSchema(many=True))
    BRANCHES = fields.Nested(BranchSchema(many=True))
    TRANSACTIONS = fields.Nested(TransactionSchema(many=True))
    PRODUCTS = fields.Nested(ProductSchema(many=True))
    PURCHASES = fields.Nested(PurchaseSchema(many=True))

    @post_load
    def make_transaction_system(self, _data, **kwargs):
        ts = TransactionSystem()

        # Making Customer Objects
        customers = []
        for customer in _data['CUSTOMERS']:
            customers.append(Customer(customer['Id'], customer['Email']))
        ts.customers = customers

        # Making Product Objects
        products = []
        for product in _data['PRODUCTS']:
            products.append(Product(product['Id'], product['Price']))
        ts.products = products

        # Making Branch Objects
        branch_ids = set()
        branches = []
        for branch in _data['BRANCHES']:
            if branch['B_Id'] not in branch_ids:
                branch_ids.add(branch['B_Id'])
                product_id = ts.get_product(branch['Pr_Id'])
                inventory = [[product_id, branch['Inventory']]]
                branches.append(Branch(branch['B_Id'], inventory))
                ts.branches = branches
            else:
                product_id = ts.get_product(branch['Pr_Id'])
                inventory = [product_id, branch['Inventory']]
                ts.get_branch(branch['B_Id']).products.append(inventory)
        ts.branches = branches

        # Making Staff Objects
        staffs = []
        for staff in _data['STAFF']:
            staffs.append(Staff(staff['Id'], staff['Email'], ts.get_branch(staff['B_Id'])))
        ts.staffs = staffs

        # Making Transaction Objects
        trans = []
        for transaction in _data['TRANSACTIONS']:
            trans.append(Transaction(transaction['T_Id'], ts.get_staff(transaction['S_Id']),
                                     ts.get_customer(transaction['C_Id']), ts.get_branch(transaction['B_Id']),
                                     transaction['DateTime']))
        ts.transactions = trans

        # Making Purchase Objects
        purchases = []
        for purchase in _data['PURCHASES']:
            purchases.append(Purchase(purchase['P_Id'], ts.get_transaction(purchase['T_Id']),
                                      ts.get_product(purchase['Pr_Id']), purchase['Quantity'],
                                      purchase['T_price']))
        ts.purchases = purchases

        # Returning the Transaction System Object
        return ts


with open('date_3.json', 'r') as json_file:
    data = json.load(json_file)

trans_schema = TransactionSystemSchema()
transaction_system = trans_schema.load(data)

print(transaction_system.branches[3])
