import json
import random
from datetime import datetime
from datetime import timedelta

TRANSACTIONS = []

product_price = [{'Id': id_, 'name': 'Product' + str(id_), 'Price': random.randint(2000, 10000)} for id_ in range(100000, 100021)]
d1 = datetime.strptime('1/1/2017 12:00 AM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2020 12:00 AM', '%m/%d/%Y %I:%M %p')
delta = d2 - d1
int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
dates = [d1 + timedelta(seconds=random.randrange(int_delta)) for i in range(2000)]
dates.sort()
staff = [{'Id': id_, 'name': 'staff' + str(id_),
          'Email': 'staff' + str(id_) + '@gmail.com',
          'B_Id': 100000 + int(str(id_)[-2])}
         for id_ in range(100000, 100100)]
customers = [{'Id': id_, 'name': 'customer' + str(id_),
              'Email': 'customer' + str(id_) + '@gmail.com'}
             for id_ in range(100000, 100100)]
BRANCHES = []
for i in range(100000, 100010):
    id_ = i
    for z in range(100000, 100021):
        dic = {'B_Id': id_, 'name': 'branch' + str(i), 'Pr_Id': z, 'Inventory': random.randint(0, 10000)}
        BRANCHES.append(dic)

for i in range(2000):
    time = str(dates[i])
    s_id = random.choice(staff)
    c_id = random.choice(customers)
    b_id = s_id['B_Id']
    dic = {
        "T_Id": i + 100000,
        "DateTime": str(time),
        "C_Id": c_id['Id'],
        "S_Id": s_id['Id'],
        "B_Id": b_id
    }
    TRANSACTIONS.append(dic)
PURCHASES = []
for i in range(4000):
    if i % 2 == 0:
        t_id = int((i / 2) + 100000)
    else:
        t_id = int(((i - 1) / 2) + 100000)
    quantity = random.randint(1, 10)
    product = random.choice(product_price)
    p_id = product['Id']
    t_price = product['Price'] * quantity

    dic = {
        "P_Id": i + 100000,
        "T_Id": t_id,
        "Pr_Id": p_id,
        "Quantity": quantity,
        "T_price": t_price
    }
    PURCHASES.append(dic)
data = {'STAFF': staff, 'CUSTOMERS': customers, 'BRANCHES': BRANCHES, 'TRANSACTIONS': TRANSACTIONS,
        'PRODUCTS': product_price, 'PURCHASES': PURCHASES}

with open('date_4.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
