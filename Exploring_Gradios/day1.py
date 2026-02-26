#!/usr/bin/env python
# coding: utf-8

# In[2]:


# imports

import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display
from dotenv import load_dotenv


# In[3]:


# Load environment variables in a file called .env
# Print the key prefixes to help with any debugging
# You can choose whichever providers you like - or all Ollama

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")


# In[4]:


# Connect to OpenAI client library
# A thin wrapper around calls to HTTP endpoints

openai = OpenAI()

# For Gemini, DeepSeek and Groq, we can use the OpenAI python client
# Because Google and DeepSeek have endpoints compatible with OpenAI
# And OpenAI allows you to change the base_url

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
ollama_url = "http://localhost:11434/v1"

gemini = OpenAI(api_key=google_api_key, base_url=gemini_url)
ollama = OpenAI(api_key="ollama", base_url=ollama_url)


# In[5]:


tell_a_joke = [
    {"role": "user", "content": "Tell a joke for a student on the journey to becoming an expert in LLM Engineering"},
]


# In[6]:


response = openai.chat.completions.create(model="gpt-4.1-mini", messages=tell_a_joke)
display(Markdown(response.choices[0].message.content))


# In[7]:


models = gemini.models.list()
for model in models:
    print(model.id)


# In[ ]:


response = gemini.chat.completions.create(model="gemini-2.5-pro", messages=tell_a_joke)
display(Markdown(response.choices[0].message.content))


# In[ ]:


easy_puzzle = [
    {"role": "user", "content": 
        "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only."},
]


# In[ ]:


response = openai.chat.completions.create(model="gpt-5-nano", messages=easy_puzzle, reasoning_effort="minimal")
display(Markdown(response.choices[0].message.content))


# In[ ]:


response = openai.chat.completions.create(model="gpt-5-nano", messages=easy_puzzle, reasoning_effort="low")
display(Markdown(response.choices[0].message.content))


# In[ ]:


response = gemini.chat.completions.create(model="gemini-2.5-pro",  messages=easy_puzzle, reasoning_effort="minimal")
display(Markdown(response.choices[0].message.content))


# In[ ]:


hard = """
On a bookshelf, two volumes of Pushkin stand side by side: the first and the second.
The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick.
A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume.
What distance did it gnaw through?
"""
hard_puzzle = [
    {"role": "user", "content": hard}
]


# In[ ]:


response = openai.chat.completions.create(model="gpt-5-nano", messages=hard_puzzle, reasoning_effort="minimal")
display(Markdown(response.choices[0].message.content))


# In[ ]:


response = gemini.chat.completions.create(model="gemini-2.5-pro", messages=hard_puzzle)
display(Markdown(response.choices[0].message.content))


# In[135]:


dilemma_prompt = """
You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice:
Cooperate: Choose "Share" — if both of you choose this, you each win $1,000.
Defect: Choose "Steal" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing.
If both steal, you both get nothing.
Do you choose to Steal or Share? Pick one.
"""

dilemma = [
    {"role": "user", "content": dilemma_prompt},
]


# In[136]:


requests.get("http://localhost:11434/").content

# If not running, run ollama serve at a command line


# In[ ]:


# Only do this if you have a large machine - at least 16GB RAM

get_ipython().system('ollama pull gpt-oss:20b')


# In[137]:


response = ollama.chat.completions.create(model="llama3.2", messages=dilemma)
display(Markdown(response.choices[0].message.content))


# In[ ]:


response = ollama.chat.completions.create(model="gpt-oss:20b", messages=dilemma)
display(Markdown(response.choices[0].message.content))


# In[ ]:


from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-lite", contents="Describe the color Blue to someone who's never been able to see in 1 sentence"
)
print(response.text)


# In[ ]:


from litellm import completion
response = completion(model="openai/gpt-4.1", messages=tell_a_joke)
reply = response.choices[0].message.content
display(Markdown(reply))


# In[ ]:


print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(f"Total cost: {response._hidden_params["response_cost"]*100:.4f} cents")


# In[ ]:


with open("hamlet.txt", "r", encoding="utf-8") as f:
    hamlet = f.read()

loc = hamlet.find("Speak, man")
print(hamlet[loc:loc+100])


# In[ ]:


question = [{"role": "user", "content": "In Hamlet, when Laertes asks 'Where is my father?' what is the reply?"}]


# In[ ]:


response = completion(model="gemini/gemini-2.5-flash-lite", messages=question)
display(Markdown(response.choices[0].message.content))


# In[ ]:


print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(f"Total cost: {response._hidden_params["response_cost"]*100:.4f} cents")


# In[ ]:


question[0]["content"] += "\n\nFor context, here is the entire text of Hamlet:\n\n"+hamlet


# In[ ]:


response = completion(model="gemini/gemini-2.5-flash-lite", messages=question)
display(Markdown(response.choices[0].message.content))


# In[ ]:


print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Cached tokens: {response.usage.prompt_tokens_details.cached_tokens}")
print(f"Total cost: {response._hidden_params["response_cost"]*100:.4f} cents")


# In[ ]:


response = completion(model="gemini/gemini-2.5-flash-lite", messages=question)
display(Markdown(response.choices[0].message.content))


# In[ ]:


print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Cached tokens: {response.usage.prompt_tokens_details.cached_tokens}")
print(f"Total cost: {response._hidden_params["response_cost"]*100:.4f} cents")


# In[ ]:


# Let's make a conversation between GPT-4.1-mini and gemini
# We're using cheap versions of models so the costs will be minimal

gpt_model = "gpt-4.1-mini"
gemini_model = "gemini-2.5-flash-lite"

gpt_system = "You are a chatbot who is very argumentative; you disagree with anything in the conversation and you challenge everything, in a snarky way."

gemini_system = "You are a very polite, courteous chatbot. You try to agree with everything the other person says, or find common ground. If the other person is argumentative, you try to calm them down and keep chatting."

gpt_messages = ["Hi there"]
gemini_messages = ["Hi"]


# In[ ]:


def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, gem in zip(gpt_messages, gemini_model):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": gem})
    response = openai.chat.completions.create(model=gpt_model, messages=messages)
    return response.choices[0].message.content


# In[ ]:


call_gpt()


# In[ ]:


def call_gemini():
    messages = [{"role": "system", "content": gemini_system}]
    for gpt, claude_message in zip(gpt_messages, gemini_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    response = gemini.chat.completions.create(model=gemini_model, messages=messages)
    return response.choices[0].message.content


# In[ ]:


call_gemini()


# In[ ]:


call_gpt()


# In[ ]:


call_gemini()


# In[ ]:


call_gpt()


# In[ ]:


gpt_messages = ["Hi there"]
gemini_messages = ["Hi"]

display(Markdown(f"### GPT:\n{gpt_messages[0]}\n"))
display(Markdown(f"### Claude:\n{gemini_messages[0]}\n"))

for i in range(3):
    gpt_next = call_gpt()
    display(Markdown(f"### GPT:\n{gpt_next}\n"))
    gpt_messages.append(gpt_next)
    
    claude_next = call_gemini()
    display(Markdown(f"### Gemini:\n{claude_next}\n"))
    gemini_messages.append(claude_next)


# In[ ]:




