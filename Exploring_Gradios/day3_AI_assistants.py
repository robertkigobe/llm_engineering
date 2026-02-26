#!/usr/bin/env python
# coding: utf-8

# In[1]:


# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr


# In[2]:


# Load environment variables in a file called .env
# Print the key prefixes to help with any debugging

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")


# In[3]:


# Initialize

openai = OpenAI()
MODEL = 'gpt-4.1-mini'


# In[4]:


# Again, I'll be in scientist-mode and change this global during the lab

system_message = "You are a helpful assistant"


# In[5]:


def chat(message, history):
    return "bananas"


# In[6]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[7]:


def chat(message, history):
    return f"You said {message} and the history is {history} but I still say bananas"


# In[8]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[9]:


def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


# In[10]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[11]:


def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


# In[12]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[14]:


system_message = "You are a helpful assistant in a clothes store. You should try to gently encourage the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. For example, if the customer says 'I'm looking to buy a hat', you could reply something like, 'Wonderful - we have lots of hats - including several that are part of our sales event.'Encourage the customer to buy hats if they are unsure what to get."


# In[15]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[16]:


system_message += "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, but remind the customer to look at hats!"


# In[17]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[18]:


def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    relevant_system_message = system_message
    if 'belt' in message.lower():
        relevant_system_message += " The store does not sell belts; if you are asked for belts, be sure to point out other items on sale."
    
    messages = [{"role": "system", "content": relevant_system_message}] + history + [{"role": "user", "content": message}]

    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


# In[19]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[ ]:




