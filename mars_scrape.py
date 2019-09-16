# Import Dependecies 
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests 

# Initialize browser
exec_path = {'executable_path': 'chromedriver.exe'}
browser = Browser("chrome", **exec_path, headless = False)

#mars = {}

# NASA MARS NEWS
def mars_news(browser):
    
 # Visit Nasa news url through splinter
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html,"html.parser")
    try:
        # Retrieve the latest element that contains news title and news_paragraph
        title = soup.find('div', class_='content_title').get_text()
        paragraph = soup.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return title, paragraph

# FEATURED IMAGE
def mars_image(browser):
    #page to be scraped
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)

    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    # Retrieve img url
    try:
        featured_image  = soup2.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        url = 'https://www.jpl.nasa.gov'
        featured_image = url + featured_image
        featured_image
    except AttributeError:
        return None
    return featured_image

# Mars Weather 
def mars_weather(browser):
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
        return weather_scrape

# Mars Facts
def mars_facts_scrape():
    try: 
        mars_df = pd.read_html("https://space-facts.com/mars/")[1]
    except BaseException:
        return None

    mars_df.columns = ['Description','Value']
    return mars_df.to_html(classes = "table table-striped")
# MARS HEMISPHERES
def mars_hemispheres(browser):
# Visit hemispheres website through splinter module 
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    html5 = browser.html
    soup5 = bs(html5, 'html.parser')
    #Create empty list for hemisphere urls
    hemisphere_urls = []

    # retrieve items that contain hemisphere info
    hemispheres = browser.find_by_css("a.product-item h3")
    #Loop through each link to get the url and title
    for link in range(len(hemispheres)):
        x = {}
        browser.find_by_css("a.product-item h3")[link].click()
        element = browser.find_link_by_text("Sample").first
        x["img_url"] = element["href"]
        x["title"] = browser.find_by_css("h2.title").text
        hemisphere_urls.append(x)
        browser.back()
    return hemisphere_urls

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=False)
    title, paragraph = mars_news(browser)
    featured_image = mars_image(browser)
    weather_scrape = mars_weather(browser)
    facts = mars_facts_scrape()
    hemisphere_urls = mars_hemispheres(browser)
   

    data = {
        "news_title": title,
        "news_paragraph": paragraph,
        "featured_image": featured_image,
        "weather": weather_scrape,
        "facts": facts,
        "hemispheres": hemisphere_urls,
        
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape())