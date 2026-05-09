data = [
    {"name": "A", "age": 25},
    {"name": "B", "age": 30},
    {"name": "C", "age": 20}
]

data = sorted(data, key=lambda x: x["age"], reverse=True)
print(data)