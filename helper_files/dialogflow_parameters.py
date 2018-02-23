import re

def para_to_dict(parameters):
    string = str(parameters)
    pattern = r'"([^"]*)"'
    m = re.findall(pattern, string)
    d = {}
    while len(m) != 0:
        d[m.pop(0)] = m.pop(1)
    print(d)
