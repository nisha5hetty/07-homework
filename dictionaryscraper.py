#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64

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

message = Mail(
    from_email=os.environ.get('FROM_EMAIL'),
    to_emails=os.environ.get('TO_EMAIL'),
    subject='Scraped content',
    html_content="It's attached as an... attachment.")

# https://www.twilio.com/blog/sending-email-attachments-with-twilio-sendgrid-python
with open('wordoftheday.csv', 'rb') as f:
    data = f.read()
    f.close()
encoded_file = base64.b64encode(data).decode()

attachedFile = Attachment(
    FileContent(encoded_file),
    FileName('wordoftheday.csv'),
    FileType('text/csv'),
    Disposition('attachment')
)
message.attachment = attachedFile

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

# In[ ]:




