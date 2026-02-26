#!/usr/bin/env python
# coding: utf-8

# 	### Text Gwnerators
# 	This code loads a pretrained GPT-2 causal language model, runs it on Apple Silicon using MPS, and generates a short continuation of text from a given prompt using Hugging Face’s high-level pipeline API.
#     •	torch: Loads PyTorch, the deep learning framework that runs the model.
# 	•	pipeline: A high-level abstraction that bundles tokenization → model inference → decoding into one call.
# 	•	AutoTokenizer: Automatically loads the correct tokenizer for the chosen model.
# 	•	AutoModelForCausalLM: Loads a causal language model (predicts the next token based only on previous tokens).

# In[2]:


import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

model_id ="gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id).to("mps")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device="mps")
result = generator("Once upon a time,", max_new_tokens=30)
print(result[0]['generated_text'])


# In[4]:


result = generator("Why did the chicken cross the road,", max_new_tokens=30)
print(result[0]['generated_text'])


# In[5]:


result = generator("Give me some nice words to a girl,", max_new_tokens=100)
print(result[0]['generated_text'])


# In[ ]:




