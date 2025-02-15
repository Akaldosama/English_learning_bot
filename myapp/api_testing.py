import requests

url = 'http://127.0.0.1:8000/api/materials/?telegram_id=1368941825&skill=listening'
#
# data = {
#     "user" : "ahahajsdkjas",
#     "message" : "akjdbabsd asdkansdas dnasdaksd kasnd ams donasn dna",
# }

res = requests.get(url)
print(res.text)
print(res.status_code)