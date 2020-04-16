# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import numpy as np
import pandas as pd 

def scrape():

    ####################
    # NASA Mars News
    ####################

    #URL to be scraped
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    #Get all the news article titles and teasers
    news_titles = soup.find_all(class_="content_title")
    news_teaser = soup.find_all(class_="rollover_description_inner")

    #Use list comprehension to pull out just the text and store in lists
    list_news_titles = [article.text.strip() for article in news_titles]
    list_news_teasers = [article.text.strip() for article in news_teaser]

    #store first article on webpage
    article_title = list_news_titles[0]

    #store first article on webpage
    article_teaser = list_news_teasers[0]

    #######################
    # JPL Mars Space Images
    #######################

    
    #Create a browser using chromedriver.exe
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    url = browser.url
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    strip = soup.find('div',class_ = 'download_tiff').text.strip()
    strip = strip[15:-4]
    featured_image_url = f'https://www.jpl.nasa.gov/spaceimages/images/largesize/{strip}_hires.jpg'

    browser.quit()

    #######################
    # Mars Weather Scrape
    #######################

    #URL to be scraped
    url = "https://twitter.com/marswxreport?lang=en"
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    tweet = soup.find('p', class_="TweetTextSize")
    tweet = tweet.text.strip()
    tweet = tweet[:-26]
    mars_weather = tweet

    #########################
    # Mars Facts Web Scraping
    #########################

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    table1 = pd.DataFrame(tables[0])
    html_table = table1.to_html(header=False, index=False)

    #########################
    # Mars Hemispheres
    #########################

    #URL to be scraped
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    hemispheres = soup.find_all('h3')

    hemisphere_list = []

    for hemisphere in hemispheres:
        hemisphere = hemisphere.text.strip()
        hemisphere_list.append(hemisphere)      
    
    dictionary_of_url = []
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    count = 1

    for hemisphere in hemisphere_list:
        browser.click_link_by_partial_text(hemisphere)
        browser.click_link_by_partial_text('Sample')
        
        browser.windows.current = browser.windows[count]
        
        image_url = browser.url

        image_dictionary = {
            "title":hemisphere,
            "img_url":image_url
        }
        
        dictionary_of_url.append(image_dictionary)

        browser.windows.current = browser.windows[0]
        
        browser.back()

        count +=1
        
    browser.quit()

    web_scrape_dictionary = {
        "mars_news_title":article_title,
        "mars_news_teaser":article_teaser,
        "jpl_image":featured_image_url,
        "mars_weather_tweet":mars_weather,
        "mars_facts_table":html_table,
        "mars_hemispheres": dictionary_of_url
    }

    print(web_scrape_dictionary)

    return web_scrape_dictionary

