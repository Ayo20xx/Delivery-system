import json

shipments= {}

with open("shipments.json") as json_file:
    data=json.load(json_file)
    for value in data:
        shipments[value["id"]]=value


print("after load" ,shipments)