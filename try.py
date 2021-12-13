from urllib.parse import quote, urlunparse
import re

url = "https://shopee.tw/【怪獸部落LitoMon】貓族-98-鮮肉主食糧800g-貓糧-鮮肉糧-主食-乾食-官方直送-效期最新-i.326491541.7659409525?sp_atk=9a81d319-17fa-4d49-90aa-da7946608e79"
m = re.search("[^(?<=https://shopee.tw/)].*", url).group()
print(m)
