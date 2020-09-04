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

# External Packages
from marshmallow import Schema, fields, post_load, ValidationError, validates, validate


class TransactionSystem:
    """This class contains the data received from the web API and has methods to perform operations"""

    def __init__(self, data_):
        self.data = data_

    def staff_details(self, id_=None):
        """Getting Staff details

        This method allows the user to query about staff details, such as number of products sold
        and total profit

        Parameters
        ----------
        id_ : int
            This is the staff ID

        Returns
        -------
        result : [list, dict]
            If the staff ID is given, then it returns a list of Total Products sold and total profit by staff
            If the staff ID is not given, then it returns a dictionary of list of Total Products sold and total
             profit by all staffs in the given data
        """

        if self.data[0]['S_Id'] is None:

            raise TypeError("Insufficient Data to get Staff details")

        # If the Id is not given, then we iterate through all the data and store the staff id in a dictionary key
        # and his details in a list
        if id_ is None:

            staff_details = {}
            for trans in self.data:

                if trans['S_Id'] not in staff_details:

                    staff_details[trans['S_Id']] = [trans['Quantity'], trans['Total_Price']]
                else:

                    staff_details[trans['S_Id']][0] += trans['Quantity']
                    staff_details[trans['S_Id']][1] += trans['Total_Price']
            return staff_details

        # If staff id is given, we iterate through all the data and return the details as a list
        _sales = 0
        _profit = 0
        for trans in self.data:
            if trans['S_Id'] == id_:
                _sales += trans['Quantity']
                _profit += trans['Total_Price']
        return [_sales, _profit]

    def customer_details(self, id_=None):
        """Getting customer details

        This method allows the user to query about customer details, such as number of products bought
        and total profit

        Parameters
        ----------
        id_ : int
            This is the customer ID

        Returns
        -------
        result : [list, dict]
            If the customer ID is given, then it returns a list of Total Products bought and total profit by customer
            If the customer ID is not given, then it returns a dictionary of list of Total Products bought and total
             profit by all customers in the given data
        """

        if self.data[0]['C_Id'] is None:
            raise TypeError("Insufficient Data to get Customer details")

        # If the Id is not given, then we iterate through all the data and store the customer id in a dictionary key
        # and his details in a list
        if id_ is None:

            customer_details = {}
            for trans in self.data:

                if trans['C_Id'] not in customer_details:

                    customer_details[trans['C_Id']] = [trans['Quantity'], trans['Total_Price']]
                else:

                    customer_details[trans['C_Id']][0] += trans['Quantity']
                    customer_details[trans['C_Id']][1] += trans['Total_Price']
            return customer_details

        # If customer id is given, we iterate through all the data and return the details as a list
        _sales = 0
        _profit = 0
        for trans in self.data:
            if trans['C_Id'] == id_:
                _sales += trans['Quantity']
                _profit += trans['Total_Price']
        return [_sales, _profit]

    def branch_details(self, b_id_=None, p_id_=None):
        """Getting Branch details

        This method allows the user to query about Inventory in a given branch for a given product

        Parameters
        ----------
        b_id_ : int
            This is the Branch ID
        p_id_ : int
            This is the Product ID

        Returns
        -------
        result : [dict, int]
            If Branch Id and Product Id are None, then returns a dictionary with keys equal to branch IDs
            and values equal to dictionary of product id and it's inventory

            If Branch Id is None and Product Id is not None, then returns a dictionary with keys equal to branch IDs
            and values equal to inventory of given product

            If Branch Id is not None and Product Id is None, then returns a dictionary with keys equal to product IDs
            and values equal to it's inventory

            If none of the above conditions match the, Branch and product IDs are given, then it returns the inventory
            of a given product in a given branch
        """

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

        if b_id_ is None and p_id_ is not None:

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
        """Getting Transaction details between given dates"""

        if self.data[0]['DateTime'] is None:
            raise TypeError("Insufficient Data (Missing DateTime) to Show Transaction Details")
        pprint(self.data)

    def __str__(self):
        return str(self.data)


class StaffSchema(Schema):
    """Validating the response from the web api for queries regarding the staff

    Returns
    -------
    TransactionSystem: Returns an instance of TransactionSystem with values of fields that are not available
                        from the response equal to None
    """

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
    """Validating the response from the web api for queries regarding the customer

    Returns
    -------
    TransactionSystem: Returns an instance of TransactionSystem with values of fields that are not available
                        from the response equal to None
    """
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
    """Validating the response from the web api for queries regarding the Branch

    Returns
    -------
    TransactionSystem: Returns an instance of TransactionSystem with values of fields that are not available
                        from the response equal to None
    """
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
    """Validating the response from the web api for queries regarding the transaction between two dates

    Returns
    -------
    TransactionSystem: Returns an instance of TransactionSystem with values of fields that are not available
                        from the response equal to None
    """
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


def log():
    """
    Creates a custom logger from the configuration dictionary
    """
    with open('SerializationLog.json', 'r') as f:
        config = json.load(f)
        logging.config.dictConfig(config)
    global logger
    logger = logging.getLogger(__name__)


def main():
    """
    Main function to do querying operations
    """

    log()

    global customer_id
    customer_id = 100247
    global staff_id
    staff_id = 100078
    global branch_id
    branch_id = 100004

    global columns
    columns = {"T_Id", "P_Id", "Quantity", "Price_Per_item", "Total_Price", "Inventory",
               "DateTime", "C_Id", "S_Id", "B_Id"}

    """with open('staff.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        staff = StaffSchema(many=True).load(data)
        s_details = staff.staff_details(staff_id)
        # print(s_details)
        print("\n---------------------------------------------------------------\n")
        print(f"Total Number of Sales by Staff: {staff_id} is {s_details[0]}")
        print(f"Total Profit by Staff: {staff_id} is {s_details[1]}")
        print("\n---------------------------------------------------------------\n")
    except ValidationError as err:
        logger.error(f"Validation Error Occurred While Loading data\n{err.messages}", exc_info=True)
    except TypeError as err:
        logger.error(f"Missing data to do requested task\n{err}", exc_info=True)

    with open('customer.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        customer = CustomerSchema(many=True).load(data)
        c_details = customer.customer_details(customer_id)
        # print(s_details)
        print(f"Total Number of Products bought by Customer: {customer_id} is {c_details[0]}")
        print(f"Total Profit by Customer: {customer_id} is {c_details[1]}")
        print("\n---------------------------------------------------------------\n")
    except ValidationError as err:
        logger.error(f"Validation Error Occurred While Loading data\n{err.messages}", exc_info=True)
    except TypeError as err:
        logger.error(f"Missing data to do requested task\n{err}", exc_info=True)
    with open('branch.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        branch = BranchSchema(many=True).load(data)
        b_details = branch.branch_details(branch_id)
        print(f"Inventory details for Branch: {branch_id}\n")
        pprint(b_details)
        print("\n---------------------------------------------------------------\n")
    except ValidationError as err:
        logger.error(f"Validation Error Occurred While Loading data\n{err.messages}", exc_info=True)
    except TypeError as err:
        logger.error(f"Missing data to do requested task\n{err}", exc_info=True)"""

    with open('date.json', 'r') as json_file:
        data = json.load(json_file)

    try:
        date = DateSchema(many=True).load(data)
        print("Transactions Between -> 1/1/2019 12:00 AM and 1/1/2020 12:00 AM\n")
        date.date_transaction()
    except ValidationError as err:
        logger.error(f"Validation Error Occurred While Loading data\n{err.messages}", exc_info=True)
    except TypeError as err:
        logger.error(f"Missing data to do requested task\n{err}", exc_info=True)


if __name__ == '__main__':
    main()
