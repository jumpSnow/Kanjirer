import re

a = "1 3 4 test"

res = re.match(r"(\d+) 3 4", a)
print(res.group(1))
