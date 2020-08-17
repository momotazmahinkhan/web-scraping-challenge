from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
import requests
import os
import time
from pprint import pprint
import pandas as pd
import urllib.request as rq
import lxml.etree as et


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #for mac users
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #return Browser("chrome", **executable_path, headless=False)
    #For windows users
    executable_path = {'executable_path': 'driver/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Store data in a dictionary
    mar_data = {
        "News" : scrape_newsh(),
        "Tweet": scrape_tweets(),
        "Image" : scrape_image(),
        "Table" : scrape_table(),
        "Hemisphere" :scrape_hemisphere(),
      }
    # Close the browser after scraping
    browser.quit()
    # Return results
    return mar_data


def scrape_tweets():
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
        #mars_weather = mars_weather.find("p", "tweet-text").text
        
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = weather_soup.find('span', text=pattern).text
    browser.quit()    
    return mars_weather

def scrape_newsh():
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

    # Get the news_headline
    news_headline = para.find("div", class_="content_title").text

    # Get the news_body
    news_para = para.find('div', class_="article_teaser_body").text

   # Store data in a dictionary
    news_data = {
        "news_headline": news_headline,
        "news_para": news_para
    }
    # Close the browser after scraping
    browser.quit()
    # Return results
    return news_data


def scrape_image():
    browser = init_browser()
    # Visit the website
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_2 = "https://www.jpl.nasa.gov"
    browser.visit(url)
    time.sleep(1)
    browser.find_by_id("full_image").click()
    browser.find_link_by_partial_text("more info").click()
    html = browser.html
    soup = bs(html, 'html.parser')
    ##relative_image_path = soup.select_one("figure.lede a img").get('src')
    relative_image_path = soup.select_one("figure.lede a img").get('src')
    featured_image_url = url_2 + relative_image_path
    # Close the browser after scraping
    browser.quit()
    # Return results
    print(featured_image_url)
    return featured_image_url

def scrape_table():
    browser = init_browser()
    # Visit visitcostarica.herokuapp.com
    url= "https://space-facts.com/mars/"
    #browser.visit(url)
    #time.sleep(5)
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description', 'Values']
    df.set_index('Description', inplace=True)
    html_table= df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    browser.quit()

    # Return results
    return html_table

##function def for hemispheres
def scrape_hemisphere():
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
    # # Close the browser after scraping
    browser.quit()     
    # Return results
    return hemisphereUrls

