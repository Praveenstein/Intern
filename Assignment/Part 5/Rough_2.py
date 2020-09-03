import json
import random

data = {"Branch": []}

product_price = [id_ for id_ in range(100000, 100021)]

for i in range(20):

    inventory = random.randint(5000, 10000)
    p_id = product_price[i]
    dic = {
            "P_Id": p_id,
            "Inventory-Left": inventory
        }
    data["Branch"].append(dic)

print(data)

with open('branch.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

