#!/usr/bin/env python
# coding: utf-8

# In[36]:


import os
from dotenv import load_dotenv
from openai import OpenAI


# In[37]:


import gradio as gr # oh yeah!


# In[38]:


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


# In[39]:


# Connect to OpenAI, Anthropic and Google; comment out the Claude or Google lines if you're not using them

openai = OpenAI()


gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"


gemini = OpenAI(api_key=google_api_key, base_url=gemini_url) 


# In[40]:


# Let's wrap a call to GPT-4.1-mini in a simple function

system_message = "You are a helpful assistant"

def message_gpt(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return response.choices[0].message.content


# In[41]:


# This can reveal the "training cut off", or the most recent date in the training data

message_gpt("What is today's date?")


# In[42]:


# here's a simple function

def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()


# In[43]:


shout("hello")


# In[44]:


gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch()


# In[45]:


# Adding share=True means that it can be accessed publically
# A more permanent hosting is available using a platform called Spaces from HuggingFace, which we will touch on next week
# NOTE: Some Anti-virus software and Corporate Firewalls might not like you using share=True. 
# If you're at work on on a work network, I suggest skip this test.

gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True)


# In[46]:


# Adding inbrowser=True opens up a new browser window automatically

gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(inbrowser=True)


# In[47]:


gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(share=True, auth=("val", "password"))


# In[48]:


# Define this variable and then pass js=force_dark_mode when creating the Interface

force_dark_mode = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""
gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never", js=force_dark_mode).launch()


# In[49]:


# Adding a little more:

message_input = gr.Textbox(label="Your message:", info="Enter a message to be shouted", lines=7)
message_output = gr.Textbox(label="Response:", lines=8)

view = gr.Interface(
    fn=shout,
    title="Shout", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=["hello", "howdy"], 
    flagging_mode="never"
    )
view.launch()


# In[50]:


# And now - changing the function from "shout" to "message_gpt"

message_input = gr.Textbox(label="Your message:", info="Enter a message for GPT-4.1-mini", lines=7)
message_output = gr.Textbox(label="Response:", lines=8)

view = gr.Interface(
    fn=message_gpt,
    title="GPT", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=["hello", "howdy"], 
    flagging_mode="never"
    )
view.launch()


# In[51]:


# Let's use Markdown
# Are you wondering why it makes any difference to set system_message when it's not referred to in the code below it?
# I'm taking advantage of system_message being a global variable, used back in the message_gpt function (go take a look)
# Not a great software engineering practice, but quite common during Jupyter Lab R&D!

system_message = "You are a helpful assistant that responds in markdown without code blocks"

message_input = gr.Textbox(label="Your message:", info="Enter a message for GPT-4.1-mini", lines=7)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=message_gpt,
    title="GPT", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=[
        "Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",
        ], 
    flagging_mode="never"
    )
view.launch()


# In[52]:


# Let's create a call that streams back results
# If you'd like a refresher on Generators (the "yield" keyword),
# Please take a look at the Intermediate Python guide in the guides folder

def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4.1-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


# In[53]:


message_input = gr.Textbox(label="Your message:", info="Enter a message for GPT-4.1-mini", lines=7)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_gpt,
    title="GPT", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=[
        "Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",
        ], 
    flagging_mode="never"
    )
view.launch()


# In[54]:


def stream_gemini(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = gemini.chat.completions.create(
        model='gemini-2.5-pro',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


# In[55]:


message_input = gr.Textbox(label="Your message:", info="Enter a message for Claude 4.5 Sonnet", lines=7)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_gemini,
    title="Claude", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=[
        "Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",
        ], 
    flagging_mode="never"
    )
view.launch()


# In[56]:


def stream_model(prompt, model):
    if model=="GPT":
        result = stream_gpt(prompt)
    elif model=="Gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result


# In[57]:


message_input = gr.Textbox(label="Your message:", info="Enter a message for the LLM", lines=7)
model_selector = gr.Dropdown(["GPT", "Gemini"], label="Select model", value="GPT")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_model,
    title="LLMs", 
    inputs=[message_input, model_selector], 
    outputs=[message_output], 
    examples=[
            ["Explain the Transformer architecture to a layperson", "GPT"],
            ["Explain the Transformer architecture to an aspiring AI engineer", "Claude"]
        ], 
    flagging_mode="never"
    )
view.launch()


# In[58]:


from scraper import fetch_website_contents


# In[59]:



# Again this is typical Experimental mindset - I'm changing the global variable we used above:

system_message = """
You are an assistant that analyzes the contents of a company website landing page
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
"""


# In[60]:


def stream_brochure(company_name, url, model):
    yield ""
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += fetch_website_contents(url)
    if model=="GPT":
        result = stream_gpt(prompt)
    elif model=="Gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result


# In[61]:


name_input = gr.Textbox(label="Company name:")
url_input = gr.Textbox(label="Landing page URL including http:// or https://")
model_selector = gr.Dropdown(["GPT", "Gemini"], label="Select model", value="GPT")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_brochure,
    title="Brochure Generator", 
    inputs=[name_input, url_input, model_selector], 
    outputs=[message_output], 
    examples=[
            ["Hugging Face", "https://huggingface.co", "GPT"],
            ["Edward Donner", "https://edwarddonner.com", "Gemini"]
        ], 
    flagging_mode="never"
    )
view.launch()


# In[ ]:





# In[ ]:




