#!/usr/bin/env python
# coding: utf-8

# In[1]:


#1 Imports
import json


# In[ ]:





# In[2]:


#2.  Simulate an LLM Tool Call Response
# Simulated response from an LLM
llm_tool_call = {
    "name": "get_weather",
    "arguments": '{"city": "London"}'  # Note: arguments as a JSON string
}


# In[3]:


#3. Parse Tool Call Arguments
# Parse the arguments JSON string into a Python dictionary
arguments = json.loads(llm_tool_call["arguments"])
print(arguments)  # Output: {'city': 'London'}


# In[4]:


#4. Access the City Value
city = arguments["city"]
print(city)  # Output: London


# In[5]:


#5. Define the Tool Function
def get_weather(city):
    # Simulate calling an external API or function
    return f"It's sunny in {city}!"


# In[6]:


#6. Call the Tool Function Using Parsed Arguments
result = get_weather(city)
print(result)  # Output: It's sunny in London!


# In[7]:


#7. (Optional) Simulate LLM Calling the Tool in a Workflow
def handle_tool_call(tool_call):
    arguments = json.loads(tool_call["arguments"])
    if tool_call["name"] == "get_weather":
        return get_weather(arguments["city"])
    else:
        return "Unknown tool"

# Simulate handling the LLM's tool call
result = handle_tool_call(llm_tool_call)
print(result)  # Output: It's sunny in London!


# In[14]:


#8. (Optional) Example: Calling an LLM with OpenAI API
# Uncomment and fill in your OpenAI API key to use this part
import openai
from dotenv import load_dotenv
import os
from openai import OpenAI


# In[15]:


load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4.1-mini"
openai = OpenAI()


# In[16]:



functions = [
     {
         "name": "get_weather",
         "description": "Get the weather for a given city.",
         "parameters": {
             "type": "object",
             "properties": {
                 "city": {"type": "string", "description": "City name"},
             },
             "required": ["city"],
         },
     }
 ]

response = openai.chat.completions.create(

     model="gpt-4-0613",
     messages=[{"role": "user", "content": "What's the weather in London?"}],
     functions=functions,
     function_call="auto"

 )
 
tool_call = response.choices[0].message.function_call
arguments = json.loads(tool_call.arguments)
result = get_weather(arguments["city"])
print(result)
 


# In[ ]:




