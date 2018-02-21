import requests
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}

r = requests.post("http://chatbots.q.att.com:19219/registerurl", params=payload)
print(r)
