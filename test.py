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

URL = "https://www.skillpipe.com/#/bookshelf/books"
LOGIN_URL = "https://www.skillpipe.com/#/account/login"

def login(browser):
    # ENTER TO LOGIN PAGE
    browser.get(LOGIN_URL)

    print(browser.title)
    print(browser.current_url)

    # WAIT FOR WEBSITE TO LOAD 
    time.sleep(10)

    # ENTER USERNAME
    username = browser.find_element_by_name("UserName")
    username.clear()
    username.send_keys(EMAIL)

    # ENTER PASSWORD
    password = browser.find_element_by_id("Password")
    password.clear()
    password.send_keys(PASSWORD)
    browser.find_element_by_id("login-button").click()

    # LOGIN
    time.sleep(3)
    if browser.current_url == URL:
        print("Logged in successfully!")

# GET CONTENT FROM A PAGE AND TRANSFORM IT TO A PDF FILE
def readPage(browser, name, bookname):
    
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
    pages = browser.find_elements_by_class_name("toc-panel__entry__title")
    for p in pages:
        print(p.get_attribute("innerHTML"))
        p.click()
        readPage(browser, p.get_attribute("innerHTML"), bookname)
        time.sleep(2)
    # browser.close()

def main():
    # SETUP FIREFOX BROWSER
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=opts)
    
    # LOGIN
    login(browser)
    
    # GET BOOKS INFO
    books = browser.find_elements_by_class_name("book--grid")
    booknames = [t.get_attribute("innerHTML") for t in browser.find_elements_by_class_name("book__text-container__code")]
    bookcount = len(books)
    
    # GO OVER EACH BOOK (NOT FINISHED)
    for b in range(bookcount):
        books[b].click()
        readBook(browser, booknames[b])
        
        # RECONNECT TO BOOK PAGE
        browser.get(URL)
        time.sleep(3)
        
        # REFRESH BOOK WEBELEMENTS
        books = browser.find_elements_by_class_name("book--grid")
    

if __name__ == '__main__':
    main()
    