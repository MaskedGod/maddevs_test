import json
from collections import defaultdict

with open("f.json", "r") as file:
    data = json.load(file)
    quantity = defaultdict(int)
    total_sum = defaultdict(int)

    for elem in data:
        category = elem["category"]
        quantity[category] += 1
        total_sum[category] += elem["price"]

print(dict(quantity))
print(dict(total_sum))
