from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd

def scrape():
  executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
  browser = Browser('chrome', **executable_path, headless=False)


  #1 Mars NASA Latest News
  new_mars = 'https://mars.nasa.gov/news/'
  browser.visit(new_mars)
  html = browser.html
  soup = bs(html, 'html.parser')

  # news_title = soup.find('div', class_="content_title").text
  news_title = soup.find('div', class_="content_title")
  news_title2 = news_title.find('a')
  news_title_text = news_title2.text
  # print(news_title_text)
  news_par = soup.find('div', class_="article_teaser_body").text
  # news_par_final = news_par.text

  # JPL Mars Space Images
  featured_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
  browser.visit(featured_url)
  html_img = browser.html
  img_soup = bs(html_img, 'html.parser')

  img_soup_img = img_soup.find(class_='carousel_item')["style"]
  base_img_url = 'https://www.jpl.nasa.gov'
  featured_image_url = base_img_url + img_soup_img.strip('background-image: url').strip(";(')")


  # Mars Twitter Weather
  m_tweets = 'https://twitter.com/marswxreport?lang=en'
  m_response = requests.get(m_tweets).text 
  mars_tweets_soup = bs(m_response, 'html.parser')

  mars_weather = mars_tweets_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.split('pic.twitter.com/')

  # Mars Fact Table
  mars_facts_url = 'https://space-facts.com/mars/'
  tables = pd.read_html(mars_facts_url)

  mars_table_facts = tables[0]
  mars_table_facts = mars_table_facts.rename(columns={0: "Description", 1: "Value"}).set_index("Description")
  mars_table_html = mars_table_facts.to_html().replace('\n', '').strip(";(')")

  # Mars Hemispheres
  hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
  hem_base_url = 'https://astrogeology.usgs.gov'
  browser.visit(hem_url)
  hem_html = browser.html
  hem_soup = bs(hem_html, 'html.parser')
  hem_links = hem_soup.find_all('div', class_='item')

  hemisphere_image_urls = []

  for links in hem_links:
      
      #Links
      #Concat links for image pages
      img_urls = hem_base_url + links.find("a", class_="itemLink product-item")['href']
      #Soup again
      browser.visit(img_urls)
      img_urls_html = browser.html
      loop_soup = bs(img_urls_html, 'html.parser')
      #Finding the links for the FULL DOWNLOAD image
      loop_links = loop_soup.find("img", class_="wide-image")['src']
      loopy_links = hem_base_url + loop_links
      
      
      #Title
      title = links.find("h3").text
      
      #Append
      hemisphere_image_urls.append({"title":title, "img_url": loopy_links})
  
  # End
  browser.quit()

  # test = "test"

  # Dictionary
  mars_dict = {
    "news_title": news_title_text,
    "news_par": news_par,
    "featured_image_url": featured_image_url,
    "mars_weather": mars_weather,
    "mars_table_html": mars_table_html,
    "hemisphere_image_urls": hemisphere_image_urls
}

  return mars_dict


