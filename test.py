import os
import time
import pdfkit
import argparse
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

# GET SKILLPIPE USER DETAILS
parser = argparse.ArgumentParser()

# -u EMAIL/USERNAME -p PASSWORD
parser.add_argument("-u", "--username", help="User name")
parser.add_argument("-p", "--password", help="Password")

args = parser.parse_args()

EMAIL = args.username
PASSWORD = args.password

LOGIN_URL = "https://www.skillpipe.com/#/account/login"

def login(browser):
    # ENTER TO LOGIN PAGE
    browser.get(LOGIN_URL)

    print(browser.title)
    print(browser.current_url)

    # WAIT FOR WEBSITE TO LOAD 
    time.sleep(10)

    # ENTER INPUT
    # USERNAME
    username = browser.find_element_by_name("UserName")
    username.clear()
    username.send_keys(EMAIL)

    # PASSWORD
    password = browser.find_element_by_id("Password")
    password.clear()
    password.send_keys(PASSWORD)
    browser.find_element_by_id("login-button").click()

    # LOGIN
    print(browser.current_url)
    time.sleep(3)
    

def readPage(browser, name, bookname):
    # get content 
    iframes = browser.find_elements_by_tag_name('iframe')
    browser.switch_to.frame(iframes[0])
    pdfkit.from_string(browser.page_source, f"books/{bookname}/{name}.pdf")
    browser.switch_to.default_content()

def readBook(browser, bookname):
    # WAIT FOR PAGE TO LOAD
    time.sleep(10)
    os.mkdir(f"books/{bookname}")
    print(browser.current_url)  
    browser.find_element_by_id("button-quickstart-toc").click()
    print(browser.current_url)  
    # pages = browser.find_elements_by_class_name("panel__list__entry--depth-2")
    titles = browser.find_elements_by_class_name("toc-panel__entry__title")
    for t in titles:
        print(t.get_attribute("innerHTML"))
        t.click()
        readPage(browser, t.get_attribute("innerHTML"), bookname)
        time.sleep(2)
    browser.close()

def main():
    # SETUP FIREFOX BROWSER
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=opts)
    
    # PAGE MENU
    
    login(browser)
    books = browser.find_elements_by_class_name("book--grid")
    # GO OVER EACH BOOK
    books[0].click()
    readBook(browser, "book1")
    

if __name__ == '__main__':
    main()
    