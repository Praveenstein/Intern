"""
Script to generate branch response
"""

import json
import random

data = []

product_price = [id_ for id_ in range(100000, 100021)]

for i in range(20):

    inventory = random.randint(0, 10000)
    dic = {
            "P_Id": product_price[i],
            "Inventory": inventory
        }
    data.append(dic)

print(data)

with open('branch.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

