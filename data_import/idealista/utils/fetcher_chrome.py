from bs4 import BeautifulSoup as bs
import random
import time
import undetected_chromedriver as uc
from urllib.parse import urlparse, parse_qs

def fetch_page(url):
    #If get the data return the html:
    #{True: html}
    #not valid
    #{False: None}
    browser = uc.Chrome()
    browser.get(url)
    time.sleep(random.randint(4, 12))

    """ Acepto las cookies """
    try:
        browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
    except:
        pass

    """ Hago scroll hacia abajo del todo para que cargue todo (imagen del mapa) """
    # time.sleep(random.randint(2, 4))
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(1, 2))
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(random.randint(2, 4))

    html = browser.page_source
    soup = bs(html, 'html.parser')
    details = soup.find_all("div",class_="details-property-feature-one")
    try:
        if str(details[0]).startswith('<div class="details-property-feature-one"'):
            return soup
        return None
    except Exception:
        return None


#For Test
# response = fetch_page('https://www.idealista.com/inmueble/93595363/')
# print(response)