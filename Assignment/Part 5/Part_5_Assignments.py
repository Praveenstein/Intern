import json

with open("pos.json", 'r') as file:
    data = json.load(file)
print(data)
