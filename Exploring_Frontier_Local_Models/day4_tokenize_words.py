#!/usr/bin/env python
# coding: utf-8

# In[4]:


import tiktoken

encoding = tiktoken.encoding_for_model("gpt-5-nano")

tokens = encoding.encode("Hi my name is Robert kigobeand I like to eat pizza")


# In[2]:


tokens


# In[5]:


for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")


# In[7]:


##Memorytestsimport os
import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI

# Load environment variables in a file called .env
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


# In[9]:


from openai import OpenAI

openai = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Robert!"}
    ]

    


# In[10]:


response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
response.choices[0].message.content


# In[11]:


messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What's my name?"}
    ]


# In[12]:


response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
response.choices[0].message.content


# In[16]:


messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi! I'm Robert!"},
    {"role": "assistant", "content": "Hi Kigobe! How can I assist you today?"},
    {"role": "user", "content": "What's my name?"}
    ]


# In[17]:


response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
response.choices[0].message.content


# In[ ]:




