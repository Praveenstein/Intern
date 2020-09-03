import json
import random
from datetime import datetime
from datetime import timedelta

data = {"Date": []}

product_price = [(id_, random.randint(2000, 10000)) for id_ in range(100000, 100021)]
d1 = datetime.strptime('1/1/2019 12:00 AM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2020 12:00 AM', '%m/%d/%Y %I:%M %p')
delta = d2 - d1
int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
dates = [d1 + timedelta(seconds=random.randrange(int_delta)) for i in range(50)]
dates.sort()

for i in range(50):

    time = str(dates[i])
    quantity = random.randint(1, 10)
    p_ = random.choice(product_price)
    p_id = p_[0]
    price = p_[1]
    dic = {
            "T_Id": random.randint(100000, 999999),
            "P_Id": p_id,
            "Quantity": quantity,
            "Price_Per_item": price,
            "Total_Price": quantity * price,
            "DateTime": str(time)
        }
    data["Date"].append(dic)

print(data)

with open('date.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

