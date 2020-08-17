# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import os
import time
from pprint import pprint
from splinter import Browser
import pandas as pd
import urllib.request as rq
import lxml.etree as et
import re


#function def 1
def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the para
    para = soup.select_one('ul.item_list li.slide')

    # Get the min avg temp
    news_headline = para.find("div", class_="content_title").text

    # Get the max avg temp
    news_para = para.find('div', class_="article_teaser_body").text

   # Store data in a dictionary
    mar_data = {
        #"sloth_img": sloth_img,
        "news_headline": news_headline,
        "news_para": news_para
    }
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mar_data

###function Def 2
def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)
    browser.find_by_id("full_image").click()
    browser.find_link_by_partial_text("more info").click()
    html = browser.html
    soup = bs(html, 'html.parser')
    ##relative_image_path = soup.select_one("figure.lede a img").get('src')
    relative_image_path = soup.select_one("figure.lede a img").get('src')
    featured_image_url = url + relative_image_path

##function def Twitter
def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    weather_soup = bs(html, 'html.parser')
    # First, find a tweet with the data-name `Mars Weather` 
    mars_weather = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"}) 
    try:
        mars_weather = mars_weather.find("p", "tweet-text").get_text()
        
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = weather_soup.find('span', text=pattern).text

#function def table
def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url= "https://space-facts.com/mars/"
    #browser.visit(url)
    #time.sleep(5)
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Values']
    html_table= df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')

##function def for hemispheres
def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url5='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    time.sleep(5)
    # create hemisphere list
    hemisphereUrls = []
    # get a list of all hemispheres
    links = browser.find_by_css("a.product-item h3")
    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
    # list all elements
        browser.find_by_css("a.product-item h3")[i].click()
    
    # find the Sample image anchor tag to get the href
        sampleImgATag = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sampleImgATag['href']
    
    # get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere to list
        hemisphereUrls.append(hemisphere)
    
    # Finally, we navigate backwards
        browser.back()

    # Store data in a dictionary
    costa_data = {
        #"sloth_img": sloth_img,
        "hemisphereUrls": hemisphereUrls
        #"news_body": news_body
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
