import hashlib

s = "dl268k"
h = hashlib.sha256(str.encode(s)).hexdigest()
print(h)
