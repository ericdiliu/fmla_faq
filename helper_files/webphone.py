import requests
import csv
import json
import re

uid="dl268k"

request_url="http://tabularasa.web.att.com/api/webphone/json/{attuid}"
profile = requests.get(request_url.format(attuid=uid))
response=profile.text
print(response)
