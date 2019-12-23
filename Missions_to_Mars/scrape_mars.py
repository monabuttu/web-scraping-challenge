#!/usr/bin/env python
# coding: utf-8

# In[126]:


from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

# In[17]:

def scrape():
        
    url = 'https://mars.nasa.gov/news/'


    # In[18]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # In[20]:

    mars_dict = {}
    
    posts = soup.find_all('li',class_='slide')

    for post in posts:
        title = post.find('h3').text
        pararaph_text= post.find('div',class_='article_teaser_body').text
        print(title)
        print(pararaph_text)

    # In[21]:

 
    news_title = soup.find(class_='content_title').get_text(strip=True)

   
    news_p = soup.find(class_='rollover_description_inner').get_text(strip=True)

   
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    # In[22]:


    browser.visit(url_2)


    # In[97]:


    html_2 = browser.html
    soup_2 = bs(html_2, 'html.parser')


    # In[109]:


    featured_image = soup_2.find('a',class_='button fancybox')
    img_url = featured_image['data-link']


    # In[110]:


    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' + img_url


    # In[111]:


    mars_dict['featured_image_url'] = featured_image_url


    # In[116]:


    url_3 = 'https://twitter.com/marswxreport?lang=en'


    # In[117]:


    browser.visit(url_3)


    # In[119]:


    html_3 = browser.html
    soup_3 = bs(html_3, 'html.parser')


    # In[123]:


    mars_weather = soup_3.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_dict['mars_weather'] = mars_weather


    # In[130]:


    url_4 = 'https://space-facts.com/mars/'


    # In[154]:


    tables = pd.read_html(url_4)
    mars_facts = tables[0]
    mars_facts.set_index(0,inplace=True)
    mars_facts.index.names = [None]
    mars_facts.columns = ['']
    html_table = mars_facts.to_html()
    html_table = html_table.replace('\n', '')
    mars_dict['html_table'] = html_table

    # In[133]:


    html_table = mars_facts.to_html()
    html_table


    # In[187]:


    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_5)
    html_5 = browser.html
    soup_5 = bs(html_5,'html.parser')


    # In[ ]:


    hemispheres = soup_5.find_all('div',class_='item')


    # In[175]:


    dict_list=[]
    dict={}
    for h in hemispheres:
        dict['title']=h.h3.text
        dict['url'] = h.a['href']
        dict_list.append(dict)
    dict_list


    # In[185]:


    hemisphere_image_urls = []

    for h in hemispheres:
        title = h.h3.text

        browser.click_link_by_partial_text(title)

        soup= bs(browser.html, 'html.parser')
        
        full = soup.find('a', text='Sample')
        
        img_url = full['href']
        
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
        browser.back()   

    browser.quit()

    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls


    # In[ ]:
    return mars_dict



