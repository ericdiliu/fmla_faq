import json

json_string = '{"status3": "Here is status 3", "status4": ["a", "b", "c"], "status5": "Here is status 5"}'

j = json.loads(json_string)

print(j['status4'][0])
