# Import Splinter and BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Create scrape all function
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': '/Users/aaranisivasekaram/.wdm/drivers/chromedriver/mac64/88.0.4324.96/chromedriver'}
    browser = Browser("chrome", **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Create function for scraping mars news site
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    # Add try-except for error handling
    try: 
        # Begin scraping article titles
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_paragraph

### Featured images

# Create function for scraping featured images site
def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try-except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None 
        
    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

### Mars Facts

# Create function for scraping mars facts website
def mars_facts():
    # Use try-except for error handling
    try:
        # Scrape table from Mars Facts website
        df = pd.read_html('http://space-facts.com/mars/')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Value']
    df.set_index('Description', inplace=True)

    # Convert dataframe back to html 
    return df.to_html()

### Hemispheres
def hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')

    for i in range(4):
    
        browser.find_by_css("a.product-item h3")[i].click()
        
        page = soup(browser.html, 'html.parser')
        
        title = page.find('h2', class_="title").get_text()
        url = page.find('a', text='Sample').get('href')
        
        hemispheres = {
            'url':url,
            'title':title
        }
        
        hemisphere_image_urls.append(hemispheres)
        
        browser.back()

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

# Complete script
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())