'''
Created on 2021/11/1

@author: janef
'''
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://shopee.tw/')
c = ';'.join(['{}={}'.format(item.get('name'), item.get('value'))
             for item in driver.get_cookies()])
print(driver.get_cookies())