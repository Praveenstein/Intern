"""
Script to generate branch response
"""
import json
TRANSACTIONS = []
BRANCHES = []
CUSTOMERS = []
STAFF = []
PRODUCTS = []
PURCHASES = []
branch_ = 100000
with open('date_4.json', 'r') as json_file:
    data = json.load(json_file)

for branch in data['BRANCHES']:
    if branch['B_Id'] == branch_:
        BRANCHES.append(branch)


for trans in data['TRANSACTIONS']:
    if trans['B_Id'] == branch_:
        TRANSACTIONS.append(trans)
staffs = set()
customers = set()
t_id = set()
for trans in TRANSACTIONS:
    staffs.add(trans['S_Id'])
    customers.add(trans['C_Id'])
    t_id.add(trans['T_Id'])


for staff in data['STAFF']:
    if staff['Id'] in staffs:
        STAFF.append(staff)

for customer in data['CUSTOMERS']:
    if customer['Id'] in customers:
        CUSTOMERS.append(customer)

pro_ids = set()

for purchase in data['PURCHASES']:
    if purchase['T_Id'] in t_id:
        PURCHASES.append(purchase)
        pro_ids.add(purchase['Pr_Id'])


for product in data['PRODUCTS']:
    if product['Id'] in pro_ids:
        PRODUCTS.append(product)

data = {'STAFF': STAFF, 'CUSTOMERS': CUSTOMERS, 'BRANCHES': BRANCHES, 'TRANSACTIONS': TRANSACTIONS,
        'PRODUCTS': PRODUCTS, 'PURCHASES': PURCHASES}

with open('branch_3.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
