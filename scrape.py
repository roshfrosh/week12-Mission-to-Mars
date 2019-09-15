# Import Dependecies 
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests 

# Initialize browser
def init_browser(): 
    # Replace the path with your actual path to the chromedriver

    #Mac Users
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #return Browser('chrome', **executable_path, headless=False)

    #Windows Users
    # executable_path = {'executable_path': '/Users/cantu/Desktop/Mission-to-Mars'}
    # return Browser('chrome', **executable_path, headless=False)
    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars = {}

# NASA MARS NEWS
def mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        

        # Visit Nasa news url through splinter
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

       html = browser.html
       soup = bs(html,"html.parser")

        # Retrieve the latest element that contains news title and news_paragraph
        title = soup.find('div', class_='content_title').get_text()
        paragraph = soup.find('div', class_="article_teaser_body").get_text()

        
        mars['news_title'] = title
        mars['news_paragraph'] = paragraph

        return mars

    finally:

        browser.quit()

# FEATURED IMAGE
def mars_image():

    try: 
        browser = init_browser()
        #page to be scraped
        img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(img_url)

        html2 = browser.html
        soup2 = bs(html_image, 'html.parser')
        # Retrieve img url
        featured_image  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        url = 'https://www.jpl.nasa.gov'
        featured_image = url + featured_image
        featured_image

        mars['featured_image_url'] = featured_image
        
        return mars
    finally:

        browser.quit()
# Mars Weather 
def mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

     
        #page to be scraped
        weather_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(weather_url)
        html3 = browser.html
        soup3 = bs(html3, 'html.parser')

        tweets = soup3.find_all('div', class_="js-tweet-text-container")
        for tweet in tweets: 
            weather_scrape = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_scrape:
                print(weather_scrape)
                break
        mars['weather_tweet'] = weather_scrape
        
        return mars
    finally:

        browser.quit()
# Mars Facts
def mars_facts_scrape():
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')

    mars_earth_comparision_df = pd.read_html(mars_facts_url)[0]
    mars_earth_comparision_df

    mars_facts = pd.read_html(mars_facts_url)[1]
    mars_facts.columns = ['Description','Value']

    mars_facts

    mars_facts_html = mars_facts.to_html()
 
    mars['mars_facts'] = mars_facts_html

    return mars
# MARS HEMISPHERES

def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(mars_hemispheres_url)
        html5 = browser.html
        soup5 = bs(html4, 'html.parser')
        #Create empty list for hemisphere urls
        hemisphere_urls = []

        # retrieve items that contain hemisphere info
        hemispheres = browser.find_by_css("a.product-item h3")
        #Loop through each link to get the url and title
        for link in range(len(hemispheres)):
            x = {}
            browser.find_by_css("a.product-item h3")[link].click()
            sample_element = browser.find_link_by_text("Sample").first
            x["img_url"] = sample_element["href"]
            x["title"] = browser.find_by_css("h2.title").text
            hemisphere_urls.append(x)
            browser.back()
        hemisphere_urls

        mars['hemispheres'] = hemisphere_urls

        return mars_info
    finally:

        browser.quit()