{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies\n",
    "from bs4 import BeautifulSoup as bs\n",
    "import requests\n",
    "from splinter import Browser\n",
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 1: Web Scraping"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## NASA Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "#URL to be scraped\n",
    "url = \"https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest\"\n",
    "# Retrieve page with the requests module\n",
    "response = requests.get(url)\n",
    "\n",
    "# Create BeautifulSoup object; parse with 'html.parser'\n",
    "soup = bs(response.text, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "#print(soup.prettify())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Get all the news article titles and teasers\n",
    "news_titles = soup.find_all(class_=\"content_title\")\n",
    "news_teaser = soup.find_all(class_=\"rollover_description_inner\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Use list comprehension to pull out just the text and store in lists\n",
    "list_news_titles = [article.text.strip() for article in news_titles]\n",
    "list_news_teasers = [article.text.strip() for article in news_teaser]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\"Mars Helicopter Attached to NASA's Perseverance Rover\""
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#store first article on webpage\n",
    "article_title = list_news_titles[0]\n",
    "article_title"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\"The team also fueled the rover's sky crane to get ready for this summer's history-making launch.\""
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#store first article on webpage\n",
    "article_teaser = list_news_teasers[0]\n",
    "article_teaser"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "def getJPL():\n",
    "    #Create a browser using chromedriver.exe\n",
    "    executable_path = {'executable_path': 'chromedriver.exe'}\n",
    "    browser = Browser('chrome', **executable_path, headless=False)\n",
    "\n",
    "    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "    browser.visit(url)\n",
    "\n",
    "    for i in range(0,1) :\n",
    "        browser.click_link_by_partial_text('FULL IMAGE')\n",
    "        browser.click_link_by_partial_text('more info')\n",
    "        url = browser.url\n",
    "        response = requests.get(url)\n",
    "        soup = bs(response.text, 'html.parser')\n",
    "        strip = soup.find('div',class_ = 'download_tiff').text.strip()\n",
    "        strip = strip[15:-4]\n",
    "        featured_image_url = f'https://www.jpl.nasa.gov/spaceimages/images/largesize/{strip}_hires.jpg'\n",
    "\n",
    "    return featured_image_url"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\mkoza\\Anaconda3\\envs\\PythonData\\lib\\site-packages\\splinter\\driver\\webdriver\\__init__.py:528: FutureWarning: browser.find_link_by_partial_text is deprecated. Use browser.links.find_by_partial_text instead.\n",
      "  FutureWarning,\n"
     ]
    }
   ],
   "source": [
    "featured_image_url = getJPL()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA14925_hires.jpg'"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "featured_image_url"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Weather Web Scraping"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "#URL to be scraped\n",
    "url = \"https://twitter.com/marswxreport?lang=en\"\n",
    "# Retrieve page with the requests module\n",
    "response = requests.get(url)\n",
    "\n",
    "# Create BeautifulSoup object; parse with 'html.parser'\n",
    "soup = bs(response.text, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "tweet = soup.find('p', class_=\"TweetTextSize\")\n",
    "tweet = tweet.text.strip()\n",
    "tweet = tweet[:-26]\n",
    "mars_weather = tweet"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Facts Web Scraping"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "url = \"https://space-facts.com/mars/\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "tables = pd.read_html(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "table1 = pd.DataFrame(tables[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "html_table = table1.to_html(header=False, index=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "#URL to be scraped\n",
    "url = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "# Retrieve page with the requests module\n",
    "response = requests.get(url)\n",
    "\n",
    "# Create BeautifulSoup object; parse with 'html.parser'\n",
    "soup = bs(response.text, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "hemispheres = soup.find_all('h3')\n",
    "\n",
    "hemisphere_list = []\n",
    "for hemisphere in hemispheres:\n",
    "    hemisphere = hemisphere.text.strip()\n",
    "    hemisphere_list.append(hemisphere)\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['Cerberus Hemisphere Enhanced',\n",
       " 'Schiaparelli Hemisphere Enhanced',\n",
       " 'Syrtis Major Hemisphere Enhanced',\n",
       " 'Valles Marineris Hemisphere Enhanced']"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hemisphere_list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "dictionary_of_url = []\n",
    "\n",
    "for hemisphere in hemisphere_list:\n",
    "    executable_path = {'executable_path': 'chromedriver.exe'}\n",
    "    browser = Browser('chrome', **executable_path, headless=False)\n",
    "\n",
    "    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "    browser.visit(url)\n",
    "    \n",
    "    browser.click_link_by_partial_text(hemisphere)\n",
    "    browser.click_link_by_partial_text('Sample')\n",
    "    \n",
    "    browser.windows.current = browser.windows[1]\n",
    "    \n",
    "    image_url = browser.url\n",
    "\n",
    "    image_dictionary = {\n",
    "        \"title\":hemisphere,\n",
    "        \"img_url\":image_url\n",
    "    }\n",
    "    \n",
    "    dictionary_of_url.append(image_dictionary)\n",
    "    \n",
    "    browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere Enhanced',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere Enhanced',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere Enhanced',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere Enhanced',\n",
       "  'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]"
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dictionary_of_url"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 2: MongoDB and Flask Application"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert all of the above code into a scrape.py file that contains the function scrape() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a MongoDB database to store the results of the scrape() function"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create an app.py file that calls scrape() and then stores the result in a MongoDB database through a (\"scrape/\") route"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create a second route (\"/\") that queries the MongoDB database and pulls out the dictionary of information"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create an index.html file that renders information from the database"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [],
   "source": [
    "# I think all of this should be performed locally? because otherwise we'd have to configure app.py to run on a server, which we haven't done yet"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:PythonData] *",
   "language": "python",
   "name": "conda-env-PythonData-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
