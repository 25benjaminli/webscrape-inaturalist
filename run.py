import requests
from bs4 import BeautifulSoup
import selenium as se
from selenium import webdriver
import os
from PIL import Image
import time

URLS = [
    "https://www.inaturalist.org/taxa/324242-Oscillatoria/browse_photos",

]


for URL in URLS:
    species_name = URL.split("/")[-2]
    print("scraping for " + species_name)
    if not os.path.exists(f'images/{species_name}'):
        os.makedirs(f'images/{species_name}')
    
    browser = webdriver.ChromeOptions()
    browser.add_argument('headless')
    browser = webdriver.Chrome(options=browser)

    # you need to scroll for the browser to load all the images
    # TODO: find a way to automatically scroll to the bottom of the page with sensing as soon as you scroll again

    browser.get(URL)
    prev_height = 0
    while prev_height < browser.execute_script("return document.body.scrollHeight"):
        prev_height = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        print("scrolling...")
    soup = BeautifulSoup(browser.page_source, "html.parser")

    
    """
    EXAMPLES:
    cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos-51218764-medium-jpg
    cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos-51218785-medium-jpg
    cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos-51218801-medium-jpg
    """

    # cover results that partially match ID
    results = soup.find_all('div', id=lambda x: x and x.startswith('cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos'))

    for result in results:
        url = result["style"].split('url(')[1].split(')')[0].replace('\"', '')
        print(url)
        img = requests.get(url)
        print(type(img))
        file = open(f'images/{species_name}/{url.split("/")[-2]}-{url.split("/")[-1]}', 'wb')
        file.write(img.content)
        file.close()