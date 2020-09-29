from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

from waitForElement import waitForElement


#1 DRIVE TO REQUESTED PAGE
#2 CHECK IF LOGIN IS NECESSARY

def isPolicyPage(driver):
    return "/user/policy.php" in driver.current_url

def isLoginRequested(driver):
    return "/login/index.php" in driver.current_url

def extractHref(text):
    sub = "href"
    start = -1
    
    for i in range(len(text)):
        if (text.startswith(sub, i)):
            start = i+6
            break
    if (start<0):
        print("error: couldn't find login page start href")
        exit(0)

    sub = "\""

    for i in range(start, len(text)):
        if (text.startswith(sub, i)):
            end = i
            break
    if (end<0):
        print("error: couldn't complete login href link")
        exit(0)
    link = text[start:end]
    return link

def clickLinkInsideInnerHTML(elem, driver, delay):
    link = extractHref(elem.get_attribute("innerHTML"))
    driver.get(link)
    time.sleep(delay)

def clickLogin(driver):
    elem = driver.find_element_by_class_name("login")
    clickLinkInsideInnerHTML(elem, driver, 5)

def clickShibbox(driver):
    elem = driver.find_element_by_id("shibbox")
    clickLinkInsideInnerHTML(elem, driver, 5)


def SSOLogin(driver, courseURL):
    while True:
        driver.get(courseURL)

        waitForElement(driver, 'guestlogin')

        if isPolicyPage(driver):
            clickLogin(driver)
            clickShibbox(driver)
            
        else:
            if (isLoginRequested(driver)):
                clickShibbox(driver)
                #exit(0)
            else:
                print("no")
                exit(0)

        if (driver.current_url == courseURL):
            break     

        while(True):
            try:

                #driver.get(sso_path)

                '''print("insert username: ")
                username = input()

                print("insert password: ")
                psw = input() '''

                waitForElement(driver, 'j_username_js')
                elem = driver.find_element_by_id('j_username_js')
                #elem.clear()
                elem.send_keys('daniel.fusaro')
                #elem.send_keys(username)
                waitForElement(driver, 'password')
                elem = driver.find_element_by_id('password')
                #elem.clear()
                elem.send_keys('Ilcielo3blu')
                #elem.send_keys(psw)
                waitForElement(driver, 'radio2')
                elem = driver.find_element_by_id('radio2')
                elem.click()

                
                waitForElement(driver, 'login_button_js')
                elem = driver.find_element_by_id('login_button_js')
                elem.click()
                break
            except Exception as err:
                print(err)

        if (driver.current_url == courseURL):
            break