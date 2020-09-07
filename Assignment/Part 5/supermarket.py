# -*- coding: utf-8 -*-
""" Main module for storing data and performing operations

This script allows the user to use the json file received from web api
and perform operation to get insights like:

    * Total sale units by a staff.
    * Total Profit by a staff.
    * Total Number of products bought by a customer.
    * Total Profit by a customer.
    * Inventory left for a given branch.
    * Transaction details between two given details.

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * schema - class for validating the responses from the web api and creating instance of TransactionSystem
    * json - To deal with Json Files
    * logging - To log Errors

"""
# Built-In Packages
import json
import logging
import logging.config

# User Packages
from schema import *

__author__ = 'praveen@gyandata.com'


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
    Main function to get data from web api, store them using transaction system class and perform operation on them.
    """

    log()

    try:
        with open('Responses\\date.json', 'r') as json_file:
            data = json.load(json_file)

        trans_schema = TransactionSystemSchema()
        transaction_system = trans_schema.load(data)

        print("\nGetting Staff Details\n--------------------------------------------------------")
        transaction_system.get_staff_details(100000)
        print("\nGetting Customer Details\n--------------------------------------------------------")
        transaction_system.get_customer_details(100000)
        print("\nGetting Transaction Details\n--------------------------------------------------------")
        transaction_system.get_transaction_details()
        print("\nGetting Staff Performance Details\n--------------------------------------------------------")
        transaction_system.get_staff_performance(100000)
        print("\nGetting Customer Value Details\n--------------------------------------------------------")
        transaction_system.get_customer_value(100000)
        print("\nGetting Branch Inventory Details\n--------------------------------------------------------")
        transaction_system.get_branch_inventory(100000)
        print("\n--------------------------------------------------------")
    except FileNotFoundError as err:
        logger.error(f"{err}")
    except LookupError as err:
        logger.error(f"{err}")
    except ValidationError as err:
        logger.error(f"Validation Error Occurred While Loading data\n{err.messages}")


if __name__ == '__main__':
    main()
