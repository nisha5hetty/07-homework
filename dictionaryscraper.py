#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[15]:


response = requests.get("https://www.merriam-webster.com/word-of-the-day/calendar")
doc = BeautifulSoup(response.text, 'html.parser')


# In[19]:


#Checking to see if it's the right section of the site
doc.select(".more-wod-items li")


# In[34]:


words = doc.select(".more-wod-items li")
for word in words:
    print("-----")
    print(word)
    print(word.select_one("h4").text)
    print(word.select_one("h2 a").text)
    print("https://www.merriam-webster.com"+word.select_one("h2 a")['href'])
    


# In[42]:


rows = []
for word in words:
    print("-----")
    row = {}
    row['date'] = (word.select_one("h4").text)
    row['word'] = (word.select_one("h2 a").text)
    row['link'] = ("https://www.merriam-webster.com"+word.select_one("h2 a")['href'])
    rows.append(row)
rows


# In[46]:


df = pd.DataFrame(rows)
df


# In[47]:


df.to_csv("wordoftheday.csv, index=False")


# In[ ]:




