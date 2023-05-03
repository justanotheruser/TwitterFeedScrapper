from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# create instance of Chrome webdriver
driver = webdriver.Chrome()
driver.get("https://twitter.com/login")

# find the element where we have to
# enter the xpath
# fill the number or mail
driver.find_element_by_xpath(
    '//*[@id ="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input').send_keys(
    'XXXXXX0418')

# find the element where we have to
# enter the xpath
# fill the password
driver.find_element_by_xpath(
    '//*[@id ="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input').send_keys(
    'PrXXXXXXXXX9')

# find the element log in
# request using xpath
# clicking on that element
driver.find_element_by_xpath(
    '//*[@id ="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div').click()