from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://shopee.tw/')
c = ';'.join(['{}={}'.format(item.get('name'), item.get('value'))
             for item in driver.get_cookies()])
token = [item.get('value') for item in driver.get_cookies()
         if item.get('name') == 'if-none-match-']
print(token)
