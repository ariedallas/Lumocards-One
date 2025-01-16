import datetime
import pprint
import json


with open ("../SUPPORT_FILES/Z_INTERNAL_CARDS/R_CardSampleRecurring.json") as fin:
    data = json.load(fin)


last = data["last occurrence"]
last_occurrence = datetime.datetime.strptime(last, '%b %d %Y, %A')

delta = last_occurrence - datetime.datetime(2024, 11, 21)
print(delta.days >= data["recurring freq"])


# pprint.pprint(data)
#
# print()
# my_dict = {
#      "a": "A"
#     ,"b": "B"
# }

# with open ("json_scratch.json", "w") as f:
#     f.write(json.dumps(my_dict, indent=2))