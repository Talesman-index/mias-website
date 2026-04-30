import os

filepath = "/Users/shalomtalesman/Mia's/index.html"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("https://wa.me/22900000000", "https://wa.me/2290151875885")
content = content.replace("WhatsApp: +229 00 00 00 00", "WhatsApp: +229 01 51 87 58 85")

with open(filepath, "w") as f:
    f.write(content)
