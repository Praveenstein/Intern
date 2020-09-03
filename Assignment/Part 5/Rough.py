import json
import random

data = {"Customer": []}

product_price = [(id_, random.randint(2000, 10000)) for id_ in range(100000, 100021)]

for i in range(50):
    quantity = random.randint(1, 10)
    p_ = random.choice(product_price)
    p_id = p_[0]
    price = p_[1]
    dic = {
            "T_Id": random.randint(100000, 999999),
            "P_Id": p_id,
            "Quantity": quantity,
            "Price_Per_item": price,
            "Total_Price": quantity * price
        }
    data["Customer"].append(dic)

print(data)

with open('Customer.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
