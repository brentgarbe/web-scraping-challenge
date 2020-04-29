from splinter import Browser
from bs4 import BeautifulSoup as bs
from time import sleep
import requests
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", headless=False) #headless = true means no browser

def scrape():

    mars_dict = {}
        
    #Sets up chromedriver with Splinter
    # Browser("chrome", headless=False)

    #Opens up a new browser if headless is "False"
    browser = init_browser()

    #Goes to NASA website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    sleep(5)
    #This checks if the element is loaded and waits 10 seconds
    if browser.is_element_present_by_css('div.content_title', wait_time=7):
        # Scrape page into Soup
        html = browser.html
        sleep(5)
        soup = bs(html, "html.parser")
        sleep(5)
        results_title = soup.find_all('div', class_="content_title")
        sleep(3)
        results_body = soup.find_all('div', class_="article_teaser_body")

        latest_title = results_title[1].text
        latest_body = results_body[0].text

        mars_dict.update({"Latest_News_Title":latest_title,"Latest_Body":latest_body})
        
    print(latest_title)
    print(latest_body)

    #This is the second portion that looks for the featured image
    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(pic_url)

    sleep(5)

    #Splinter function to locate button on page
    results = browser.find_by_id('full_image')
    img = results[0]
    img.click()
    sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url = soup.find("img", class_="fancybox-image")['src']

    full_url = (f'{base_url}{featured_image_url}')

    mars_dict.update({"Featured_Image":full_url})
    print(full_url)

    #This scrapes Twitter for weather on Mars
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    #You get xpath by inspecting the element and doing copy full xpath
    xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span'

    if browser.is_element_present_by_xpath(xpath, wait_time=5):
        first_tweet = browser.find_by_xpath(xpath)
        html = first_tweet.html
        soup = bs(html, 'html.parser')

        mars_current_weather = str(soup)

    mars_dict.update({"Mars_Current_Weather":mars_current_weather})
    print(mars_current_weather)

    #Visit the Mars Facts webpage here and use Pandas to scrape the table 
    #containing facts about the planet including Diameter, Mass, etc.
    mars_read = pd.read_html('https://space-facts.com/mars/')
    
    #Mars Facts
    mars_facts = mars_read[0]
    mars_html = mars_facts.to_html(index=False, header=False)
    print(mars_facts)

    mars_dict.update({"Mars_Facts":mars_html})

    #This is a big loop that gathers 4 images and stores the data into 
    #a dictionary and then that dictionary into a list
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    sleep(5)

    #This runs a for loop to look for the 4 hemisperes. It saves the jpeg link and title into a dictionary
    lists=[]
    titles = {}
    for x in range(0,4):
        
        #Revisits the website each time
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        sleep(5)
        
        #This goes to each of the four links that 
        browser.find_by_tag('h3')[x].click()

        html = browser.html
        soup = bs(html, 'html.parser')

        sleep(3)

        #This finds the download box where the jpg is stored
        results = soup.find_all('div', class_='downloads')
        links = results[0].find('li').a['href']
        
        titles = soup.find_all('h2', class_='title')
        title = titles[0].text
        
        othername={"Title":title,"img URL":links}
        lists.append(othername)

    mars_dict.update({"Mars_Hemispheres":lists})
    print(lists)

    return mars_dict
    

