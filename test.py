import re

url = "https://shopee.tw/【怪獸部落LitoMon】貓族-98-鮮肉主食糧800g-貓糧-鮮肉糧-主食-乾食-官方直送-效期最新-i.326491541.7659409525?sp_atk=4d710b8c-2472-4860-9cba-7a413aca0537"
m = re.search("\-i\..*", url).group()
print(m)
