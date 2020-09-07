# -*- coding: utf-8 -*-
""" Classes for the transaction system

This module has class for storing the transaction details and performing operations using them.

This file contains the following Classes:

    * Staff - This class contains the data of the staff.
    * Customer - This class contains the data of the customer.
    * Transaction - This class contains the data of the transaction.
    * Product - This class contains the data of the product.
    * Purchase - This class contains the data of the purchase.
    * TransactionSystem - This class contains the data of the whole transaction system.

"""

__author__ = 'praveen@gyandata.com'


class Staff:
    """
    Staff Class with associated information.

    ...

    Attributes
    ----------
    id : int
        Staff Id.

    email : Str
        Staff Email.

    branch : Branch
        Reference to an instance of branch class, representing the branch to which the
        staff belongs to.
    """
    def __init__(self, id_, name, email, branch_):

        self.name = name
        self.id = id_
        self.email = email
        self.branch = branch_

    def __str__(self):
        return f"Staff name: {self.name}, Email: {self.email}, Branch Id: {self.branch.id}"


class Customer:
    """
    Customer Class with associated information.

    ...

    Attributes
    ----------
    id : int
        Customer Id.

    email : Str
        Customer Email.
    """
    def __init__(self, id_, name, email):
        self.name = name
        self.id = id_
        self.email = email

    def __str__(self):
        return f"Customer name: {self.name}, Email: {self.email}"


class Branch:
    """
    Branch Class with associated information.

    ...

    Attributes
    ----------
    id : int
        Customer Id.

    products : list
        List consisting of list of product (Instance of Product Class) reference,
        and its inventory details for the product.
    """
    def __init__(self, id_, name, products_):
        self.name = name
        self.id = id_
        self.products = products_

    def __str__(self):
        return f"Branch Id: {self.id}"


class Transaction:
    """
    Transaction Class with associated information.

    ...

    Attributes
    ----------
    id : int
        Customer Id.

    staff : list
        List consisting of Staffs (Instance of Staff Class) reference.

    customer : list
        List consisting of Customers (Instance of Customer Class) reference.

    branch : list
        List consisting of branches (Instance of Branch Class) reference.

    datetime : datetime
        The datetime during which the transaction occurred.
    """
    def __init__(self, id_, staff_, customer_, branch_, _datetime):
        self.id = id_
        self.staff = staff_
        self.customer = customer_
        self.branch = branch_
        self.datetime = _datetime

    def __str__(self):
        return f"Transaction Id: {self.id}, Handling Staff: {self.staff.id}, " \
               f" Customer: {self.customer.id}, Handling Branch: {self.branch.id}, Date: {self.datetime}"


class Product:
    """
    Product Class with associated information.

    ...

    Attributes
    ----------
    id : int
        Customer Id.

    price : float
        Price of the product.
    """
    def __init__(self, id_, name, price):
        self.name = name
        self.id = id_
        self.price = price

    def __str__(self):
        return f"Product Id: {self.id}, Price Per Product: {self.price}"


class Purchase:
    """
    Purchase Class with associated information.

    ...

    Attributes
    ----------
    id : int
        Customer Id.

    transaction : Transaction
        A reference to an instance of Transaction class which occurred in this purchase.

    product : Product
        A reference to an instance of Product class which occurred in this purchase.

    quantity : int
        Number of quantity of products purchased.

    total_price : float
        Total Price in this purchase.
    """
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
    """
    TransactionSystem class with associated information.

    ...

    Attributes
    ----------
    staffs : list
        List consisting of references to staffs (Instance of Staff Class).

    customers : list
        List consisting of references to customers (Instance of Customer Class).

    branches : list
        List consisting of references to branches (Instance of Branch Class).

    transactions : list
        List consisting of references to transactions (Instance of Transaction Class).

    products : list
        List consisting of references to products (Instance of Product Class).

    purchases : list
        List consisting of references to purchases (Instance of Purchase Class).

    Methods
    -------
    get_staff(id_)
        Returns the reference to Staff object whose Id matches id_.

    get_customer(id_)
        Returns the reference to Customer object whose Id matches id_.

    get_branch(id_)
        Returns the reference to Branch object whose Id matches id_.

    get_transaction(id_)
        Returns the reference to Transaction object whose Id matches id_.

    get_purchase(id_)
        Returns the reference to Purchase object whose Id matches id_..

    get_product(id_)
        Returns the reference to Product object whose Id matches id_.

    get_staff_details(id_)
        Displays the Staff Details such as the transactions he was involved, customer handled.

    get_customer_details(id_)
        Displays the Customer Details such as the transactions he was involved, staff who handled.

    get_transaction_details()
        Displays the Transaction Details between two dates such as the Products and Purchase involved.

    get_staff_performance(id_)
        Displays the Staff's Total sales and monetary value.

    get_customer_value(id_)
        Displays the Customer's Total number of products bought and monetary value.

    get_branch_inventory(id_)
        Displays the Inventory details of products in the given branch.

    Raises
    ------
    LookupError
        If Id (Product Id, Branch Id, etc) is not found.

    """
    def __init__(self):
        self.staffs = []
        self.customers = []
        self.branches = []
        self.transactions = []
        self.products = []
        self.purchases = []

    def get_staff(self, id_):
        """
        Finding the Staff

        ...

        Parameters
        ----------
        id_ : int
            Id of the staff.

        """
        for _staff in self.staffs:
            if _staff.id == id_:
                return _staff
        raise LookupError("Staff Not in DB")

    def get_customer(self, id_):
        """
        Finding the Customer

        ...

        Parameters
        ----------
        id_ : int
            Id of the customer.

        """
        for _customer in self.customers:
            if _customer.id == id_:
                return _customer
        raise LookupError("customer Not in DB")

    def get_branch(self, id_):
        """
        Finding the Branch

        ...

        Parameters
        ----------
        id_ : int
            Id of the branch.

        """
        for _branch in self.branches:
            if _branch.id == id_:
                return _branch
        raise LookupError("Branch Not in DB")

    def get_transaction(self, id_):
        """
        Finding the Transaction

        ...

        Parameters
        ----------
        id_ : int
            Id of the transaction.

        """
        for _transaction in self.transactions:
            if _transaction.id == id_:
                return _transaction
        raise LookupError("Transaction Not in DB")

    def get_purchase(self, id_):
        """
        Finding the Purchase

        ...

        Parameters
        ----------
        id_ : int
            Id of the purchase.

        """
        for _purchase in self.purchases:
            if _purchase.id == id_:
                return _purchase
        raise LookupError("Purchase Not in DB")

    def get_product(self, id_):
        """
        Finding the Product

        ...

        Parameters
        ----------
        id_ : int
            Id of the product.

        """
        for _product in self.products:
            if _product.id == id_:
                return _product
        raise LookupError("Product Not in DB")

    def get_staff_details(self, _id):
        """
        Getting the staff details

        ...

        Parameters
        ----------
        _id : int
            Id of the staff.

        """
        _data = f"The Transactions Handled by Staff: {self.get_staff(_id).name}\n-------------------------------------\n"
        _match = False
        for _trans in self.transactions:
            if _trans.staff.id == _id:
                _match = True
                _data += f"Transaction Id: {_trans.id}\nCustomer: {_trans.customer.name}\n" \
                         f"Handling Branch: {_trans.branch.name}\nDate: {_trans.datetime}\n" \
                         f"\n-------------------------------------\n"
        if not _match:
            raise LookupError("Staff Not in DB")
        print(_data)

    def get_customer_details(self, _id):
        """
        Getting the customer details

        ...

        Parameters
        ----------
        _id : int
            Id of the staff.

        """
        _data = f"The Transactions In which the Customer: {self.get_customer(_id).name}" \
                f" was involved:\n-------------------------------------\n"
        _match = False
        for _trans in self.transactions:
            if _trans.customer.id == _id:
                _match = True
                _data += f"Transaction Id: {_trans.id}\nStaff: {_trans.staff.name}\n" \
                         f"Handling Branch: {_trans.branch.name}\nDate: {_trans.datetime}\n" \
                         f"-------------------------------------\n"
        if not _match:
            LookupError("Customer Not in DB")
        print(_data)

    def get_transaction_details(self):
        """ Getting the transaction details """

        _data = f"The Transactions Details are\n-------------------------------------\n"
        for _trans in self.transactions:
            print(f"\nFor the Transaction: {_trans.id}")
            for _purchase in self.purchases:
                if _purchase.transaction.id == _trans.id:
                    print(f"\nPurchase Id: {_purchase.id}\nProduct Id: {_purchase.product.name}\n"
                          f"Quantity: {_purchase.quantity}"
                          f"\nTotal Price: {_purchase.total_price}")
            print("\n-------------------------------------\n")

    def get_staff_performance(self, _id):
        """ Getting the staff performance details """
        _quantity = 0
        _total_price = 0
        _match = False
        for _trans in self.transactions:
            if _trans.staff.id == _id:
                _match = True
                for _purchase in self.purchases:
                    if _purchase.transaction.id == _trans.id:
                        _quantity += _purchase.quantity
                        _total_price += _purchase.total_price
        if not _match:
            raise LookupError("Staff Not in DB")

        print(f"The Number of Products sold by Staff {self.get_staff(_id).name} is"
              f" {_quantity} and Total Monetary Value: {_total_price}")

    def get_customer_value(self, _id):
        """ Getting the customer value details """
        _quantity = 0
        _total_price = 0
        _match = False
        for _trans in self.transactions:
            if _trans.customer.id == _id:
                _match = True
                for _purchase in self.purchases:
                    if _purchase.transaction.id == _trans.id:
                        _quantity += _purchase.quantity
                        _total_price += _purchase.total_price
        if not _match:
            raise LookupError("Customer Not in DB")

        print(f"The Number of Products Bought by Customer {self.get_customer(_id).name} is {_quantity}"
              f" and Total Monetary Value: {_total_price}")

    def get_branch_inventory(self, _id):
        """ Getting the branch inventory details """
        _branch = self.get_branch(_id)
        print(f"\n\nThe Inventory Details for Branch:"
              f" {self.get_branch(_id).name}\n--------------------------------\n\n")
        for _product in _branch.products:
            print(f"The Inventory for Product: {_product[0].id} is {_product[1]}")
