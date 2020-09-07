# -*- coding: utf-8 -*-
""" Schema Classes

This module has class for validating the responses from the web api and creating instance of TransactionSystem.

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * marshmallow - lightweight Object serialization and deserialization package.
    * transaction - To store transaction details and perform operations on them.

This file contains the following Classes:

    * StaffSchema - This class validates the staff details from the response.

    * CustomerSchema - This class validates the customer details from the response.

    * BranchSchema - This class validates the branch details from the response.

    * TransactionSchema - This class validates the transaction details from the response.

    * ProductSchema - This class validates the products details from the response.

    * PurchaseSchema - This class validates the purchase details from the response.

    * TransactionSystemSchema - This class validates the full data from the response by nesting
      the above schema classes.

"""

# User Packages
from transaction import Staff, Customer, Branch, Transaction, Product, Purchase, TransactionSystem

# External Packages
from marshmallow import Schema, fields, post_load, ValidationError, validates, validate

__author__ = 'praveen@gyandata.com'


class StaffSchema(Schema):
    """This class validates the staff details from the response."""

    Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    Email = fields.Email(required=True)
    B_Id = fields.Integer(validate=validate.Range(100000, 100010), required=True)
    name = fields.String(required=True)


class CustomerSchema(Schema):
    """This class validates the customer details from the response."""

    Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    Email = fields.Email(required=True)
    name = fields.String(required=True)


class BranchSchema(Schema):
    """This class validates the branch details from the response."""

    B_Id = fields.Integer(validate=validate.Range(100000, 100010), required=True)
    Pr_Id = fields.Integer(validate=validate.Range(100000, 100021), required=True)
    Inventory = fields.Integer(required=True)
    name = fields.String(required=True)

    @validates('Inventory')
    def validate_inventory(self, _inventory):
        if _inventory < 0:
            raise ValidationError('Inventory Cannot Be Negative')


class TransactionSchema(Schema):
    """This class validates the transaction details from the response."""

    T_Id = fields.Integer(validate=validate.Range(100000, 102000), required=True)
    DateTime = fields.DateTime(format="%Y-%m-%d %H:%M:%S", required=True)
    C_Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    S_Id = fields.Integer(validate=validate.Range(100000, 100100), required=True)
    B_Id = fields.Integer(validate=validate.Range(100000, 100010), required=True)


class ProductSchema(Schema):
    """This class validates the product details from the response."""

    Id = fields.Integer(validate=validate.Range(100000, 100021), required=True)
    Price = fields.Float(required=True)
    name = fields.String(required=True)

    @validates('Price')
    def validate_price(self, _price):
        if _price <= 0:
            raise ValidationError('Price Cannot be Zero or less')


class PurchaseSchema(Schema):
    """This class validates the purchase details from the response."""

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
    """This class validates the full data from the response by nesting the above schema classes.
    Returns
    -------
    TransactionSystem
        Populates the transaction system class with data from response and returns an instance of it.
    """

    STAFF = fields.Nested(StaffSchema(many=True))
    CUSTOMERS = fields.Nested(CustomerSchema(many=True))
    BRANCHES = fields.Nested(BranchSchema(many=True))
    TRANSACTIONS = fields.Nested(TransactionSchema(many=True))
    PRODUCTS = fields.Nested(ProductSchema(many=True))
    PURCHASES = fields.Nested(PurchaseSchema(many=True))

    @post_load
    def make_transaction_system(self, _data, **kwargs):
        """Creating instance of Transaction System

        Parameters
        ----------
        _data : json
            Json response from the web api.
        Returns
        -------
        TransactionSystem
            Populates the transaction system class with data from response and returns an instance of it.
        """
        ts = TransactionSystem()

        # Making Customer Objects
        customers = []
        for customer in _data['CUSTOMERS']:
            customers.append(Customer(customer['Id'], customer['name'], customer['Email']))
        ts.customers = customers

        # Making Product Objects
        products = []
        for product in _data['PRODUCTS']:
            products.append(Product(product['Id'], product['name'], product['Price']))
        ts.products = products

        # Making Branch Objects
        branch_ids = set()
        branches = []
        for branch in _data['BRANCHES']:
            if branch['B_Id'] not in branch_ids:
                branch_ids.add(branch['B_Id'])
                product_id = ts.get_product(branch['Pr_Id'])
                inventory = [[product_id, branch['Inventory']]]
                branches.append(Branch(branch['B_Id'], branch['name'], inventory))
                ts.branches = branches
            else:
                try:
                    product_id = ts.get_product(branch['Pr_Id'])
                    inventory = [product_id, branch['Inventory']]
                    ts.get_branch(branch['B_Id']).products.append(inventory)
                except LookupError:
                    continue
        ts.branches = branches

        # Making Staff Objects
        staffs = []
        for staff in _data['STAFF']:
            staffs.append(Staff(staff['Id'], staff['name'], staff['Email'], ts.get_branch(staff['B_Id'])))
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

