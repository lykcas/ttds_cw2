import re

str = "#hash.eifhdsj ewhsfd soooooohapppppppy"
str2 = "sooooooohappy"
patt = '#(\w+)'
patt2 = r'(.)\1{1,}'
arr = re.findall(patt, str)
arr2 = re.findall(patt2, str)
arr2_2 = re.findall(patt2, str2)
arr2_1 = re.sub(r'(.)\1{2,}', r'\1\1\1', str)