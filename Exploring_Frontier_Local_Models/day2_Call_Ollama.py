#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
from dotenv import load_dotenv
from IPython.display import Markdown, display

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


# In[9]:


import requests

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

payload = {
    "model": "gpt-5-nano",
    "messages": [
        {"role": "user", "content": "create me a backend for springboot to manage my notes"}]
}

payload


# In[10]:


response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=payload
)

response.json()


# In[11]:


summary = response.json()["choices"][0]["message"]["content"]


# In[12]:


# Step 4: Print/display the result
def display_summary():
    """Get and display the summary in Markdown format."""
    
    try:
        display(Markdown(summary))  # For Jupyter notebooks
    except:
        print(summary)  # For regular Python scripts
    
    return summary

    


# In[13]:


summary = display_summary()


# In[14]:


# The shortest way to get the summary

# Create OpenAI client

from openai import OpenAI
openai = OpenAI()

response = openai.chat.completions.create(model="gpt-5-nano", messages=[{"role": "user", "content": "Tell me a fun fact"}])

response.choices[0].message.content


# In[18]:


## And Ollama also gives an OpenAI compatible endpoint


# In[ ]:


requests.get("http://localhost:11434").content


# In[19]:


get_ipython().system('ollama pull llama3.2')


# In[21]:


OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(base_url=OLLAMA_BASE_URL,api_key='ollama')
response = ollama.chat.completions.create(model="llama3.2", messages=[{"role": "user", "content": "Tell me a fun fact"}])

response.choices[0].message.content


# In[23]:


## Deepseek 
get_ipython().system('ollama pull deepseek-r1:1.5b')


# In[24]:


response = ollama.chat.completions.create(model="deepseek-r1:1.5b", messages=[{"role": "user", "content": "Tell me a fun fact"}])

response.choices[0].message.content


# In[ ]:




