from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from OSUtilities import isFile

import pickle
from waitForElement import waitForElement

import time

from config import *

class SSOLogin:
    def __init__(self, driver):
        self.driver = driver

    def isPolicyPage(self):
        return "/user/policy.php" in self.driver.current_url

    def isLoginRequested(self):
        return "/login/index.php" in self.driver.current_url

    def isEnrolPage(self):
        return "/enrol/" in self.driver.current_url

    def extractHref(self, text):
        sub = "href"
        start = -1
        
        for i in range(len(text)):
            if (text.startswith(sub, i)):
                start = i+6
                break
        if (start<0):
            print("error: couldn't find login page start href")
            self.driver.quit()
            exit(0)

        sub = "\""

        for i in range(start, len(text)):
            if (text.startswith(sub, i)):
                end = i
                break
        if (end<0):
            print("error: couldn't complete login href link")
            self.driver.quit()
            exit(0)
        link = text[start:end]
        return link

    def clickLinkInsideInnerHTML(self, elem, delay):
        link = self.extractHref(elem.get_attribute("innerHTML"))
        self.driver.get(link)

    def clickLogin(self):
        elem = self.driver.find_element_by_class_name("login")
        self.clickLinkInsideInnerHTML(elem, 5)

    def clickShibbox(self):
        elem = self.driver.find_element_by_id("shibbox")
        self.clickLinkInsideInnerHTML(elem, 5)

    def loginSequence(self, username=None, psw=None):
        waitForElement(self.driver, 'j_username_js')
        elem = self.driver.find_element_by_id('j_username_js')
        if username==None:
            username = input()
        elem.send_keys(username)
        waitForElement(self.driver, 'password')
        elem = self.driver.find_element_by_id('password')
        if psw==None:
            psw = input()
        elem.send_keys(psw)
        waitForElement(self.driver, 'radio2')
        elem = self.driver.find_element_by_id('radio2')
        elem.click()

        waitForElement(self.driver, 'login_button_js')
        elem = self.driver.find_element_by_id('login_button_js')
        elem.click()

    def login(self, courseURL):
        flag = False
        if (isFile("driver.pkl")):
            try:
                with open("driver.pkl", "rb") as f:
                    date, cookies = pickle.load(f)
                    if (time.time()-date<COOKIE_EXPIRY_ESTIMATE):
                        print("COOKIES are acceptable")
                        self.driver.get(courseURL)
                        self.driver.delete_all_cookies()
                        for cookie in cookies:
                            self.driver.add_cookie(cookie)
                        self.driver.get(courseURL)
                        waitForElement(self.driver, 'page')
                        if (self.driver.current_url == courseURL):
                            flag = True
            except:
                pass
        if flag:
            return
        print("COOKIES are NOT acceptable")
        while True:
            self.driver.get(courseURL)

            if (self.driver.current_url == courseURL):
                break
            time.sleep(2)

            if self.isPolicyPage() or self.isEnrolPage():
                self.clickLogin()
                self.clickShibbox()
                
            else:
                if (self.isLoginRequested()):
                    self.clickShibbox()
                else:
                    print("no Shibbox login has been found.\n" /
                        +"Consider redoing the cycle of ssologin\n" /
                        +"Aborting...")
                    exit(0)

            if (self.driver.current_url == courseURL):
                break

            while(True):
                try:
                    if (self.driver.current_url == courseURL):
                        break
                    if (isFile("data/credentials.txt")):
                        with open("data/credentials.txt", "r") as f:
                            username = f.readline()[:-1]
                            psw = f.readline()
                            self.loginSequence(username, psw)
                    else:
                        self.loginSequence()
                    waitForElement(self.driver, modeinfo="//div[@class='usermenu']", mode="xpath")
                    break
                except Exception as err:
                    print("some error occurred")
                    print(err)
            time.sleep(1)
            if (self.driver.current_url == courseURL):
                break