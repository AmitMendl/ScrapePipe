from cgitb import reset
import os
import time
# import pdfkit
import argparse
from xhtml2pdf import pisa
from selenium import webdriver
from PyPDF2 import PdfFileMerger
from selenium.webdriver import FirefoxOptions

# GET SKILLPIPE USER DETAILS
parser = argparse.ArgumentParser()

# -u EMAIL/USERNAME -p PASSWORD
parser.add_argument("-u", "--username", help="Skillpipe username/email")
parser.add_argument("-p", "--password", help="SKillpipe password")

args = parser.parse_args()

EMAIL = args.username
PASSWORD = args.password

URL = "https://www.skillpipe.com/#/bookshelf/books"
LOGIN_URL = "https://www.skillpipe.com/#/account/login"

# LOGIN TO SKILLPIPE
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
    time.sleep(10)
    if browser.current_url == URL:
        print("Logged in successfully!")

# SAVE PAGE AS PDF FILE
def readPage(browser, name, bookname):    
    
    iframes = browser.find_elements_by_tag_name('iframe')
    browser.switch_to.frame(iframes[0])
    
    #XHTML2PDF
    page_file = open(f"books/{bookname}/{name}.pdf", 'w+b')
    pisa_status = pisa.CreatePDF(
            browser.page_source,        # the HTML to convert
            dest=page_file              # file handle to recieve result
    )
    page_file.close()
    
    result = pisa_status.err

    if not result:
        print("Successfully created PDF")
    else:
        print("Error: unable to create the PDF") 

    # pdfkit.from_string(browser.page_source, f"books/{bookname}/{name}.pdf")
    browser.switch_to.default_content()
    
    return result

# GET CONTENT FROM A PAGE AND TRANSFORM IT TO A PDF FILE
def readBook(browser, bookname):
    
    # WAIT FOR PAGE TO LOAD
    time.sleep(15)
    os.mkdir(f"books/{bookname}")
    browser.find_element_by_id("button-quickstart-toc").click()
    
    # GET PAGES OF BOOKS
    pages = browser.find_elements_by_class_name("toc-panel__entry__title")
    print(f"Downloading {bookname}...")
    # READ PAGES
    for p in pages:
        # print(p.get_attribute("innerHTML"))
        p.click()
        readPage(browser, p.get_attribute("innerHTML"), bookname)
        time.sleep(3)
        
    print(f"Merging {bookname}...")
    mergepages(bookname)

def mergepages(bookname):
    
    merger = PdfFileMerger()
    
    # MERGE FILES
    files = os.listdir(f"books/{bookname}")
    for file in files:
        merger.append(open(f"books/{bookname}/{file}", 'rb'))
        # DELETE MERGED FILE
        # os.remove(file)
    
    # CREATE THE MERGED FILE
    with open(f"books/{bookname}.pdf", "wb") as fout:
        merger.write(fout)
        
    # os.rmdir(f"books/{bookname}")


def main():
    # SETUP FIREFOX BROWSER
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=opts)
    
    # LOGIN
    login(browser)
    
    # GET BOOKS INFO
    books = browser.find_elements_by_class_name("book--grid")[:1]
    booknames = [t.get_attribute("innerHTML") for t in browser.find_elements_by_class_name("book__text-container__code")]
    bookcount = len(books)
    
    # GO OVER EACH BOOK (NOT FINISHED)
    for b in range(bookcount):
        time.sleep(5)
        books[b].click()
        readBook(browser, booknames[b])
        
        # RECONNECT TO BOOK PAGE
        browser.get(URL)
        time.sleep(5)
        
        # REFRESH BOOK WEBELEMENTS
        books = browser.find_elements_by_class_name("book--grid")
    

if __name__ == '__main__':
    main()
    