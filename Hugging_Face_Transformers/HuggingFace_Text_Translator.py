#!/usr/bin/env python
# coding: utf-8

# 	### Text Translator
# 	This code loads a pretrained GPT-2 causal language model, runs it on Apple Silicon using MPS, and generates a short continuation of text from a given prompt using Hugging Face’s high-level pipeline API.
#     •	torch: Loads PyTorch, the deep learning framework that runs the model.
# 	•	pipeline: A high-level abstraction that bundles tokenization → model inference → decoding into one call.
# 	•	AutoTokenizer: Automatically loads the correct tokenizer for the chosen model.
# 	•	AutoModelForCausalLM: Loads a causal language model (predicts the next token based only on previous tokens).

# 

# In[5]:


pip install sentencepiece


# In[3]:


import torch
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

model_id ="Helsinki-NLP/opus-mt-en-fr"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to("mps")
translator = pipeline("translation_en_to_fr", model=model, tokenizer=tokenizer, device="mps")
result = translator("The weather is nice today")
print(result[0]['translation_text'])


# In[ ]:




