from splinter import Browser
import requests
import pymongo
from bs4 import BeautifulSoup
import pandas as pd
import time



def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

### Mars site
def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    

    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

  ## Mars space images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html =browser.html
    image_soup= BeautifulSoup(html, 'html.parser')

    period = image_soup.find_all(class_="carousel_container")
    one =period[0]
    #print(one.prettify())
    img = one.find("a")
    image = img['data-fancybox-href']
    featured_image = image_url+image
    featured_image


## Mars Facts
    url = "https://space-facts.com/mars/"
    facts = pd.read_html(url)
    facts_col = facts[0]
    facts_col.columns = ['Description','Dimensions']
    mars_facts=facts_col.to_html()

## Mars Hemisphere

    usgs="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs)
    html =browser.html
    usgs_soup= BeautifulSoup(html, 'html.parser')

    container = usgs_soup.find_all("div", class_="item")
    usgs_url = "https://astrogeology.usgs.gov"
    titles = []
    images= []
    title_img =[]
    for item in container:
        title = item.find("h3").text
        titles.append(title)
        image =usgs_url + item.find("img", class_='thumb')['src']
        images.append(image)
        title_img.append({"title" : title, "img_url" : image})
    # images

    hemisphere_image_urls = title_img
    hemisphere_image_urls

    mars_details = {
      "news_title": news_title,
      "news_p": news_p,
      "featured_image": featured_image,
      "mars_facts" : mars_facts,
      "Mars_Hemisphere": hemisphere_image_urls

    }


    return mars_details

    