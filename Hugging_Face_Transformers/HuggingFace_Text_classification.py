#!/usr/bin/env python
# coding: utf-8

# 	This code runs sentiment analysis on a sentence using a pretrained BERT-style classifier, accelerated on Apple Silicon (MPS). Let’s break it down step by step.
#    	•	PyTorch (torch) Provides the tensor engine and model execution.
# 		Hugging Face Transformers
# 	•	AutoTokenizer: converts text → tokens
# 	•	AutoModelForSequenceClassification: loads a classifier head on top of a transformer
# 	•	pipeline: wraps preprocessing, inference, and postprocessing into one call

# In[1]:


import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

model_id ="distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id).to("mps")
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device="mps")
result = classifier("I love using AI on my mac")
print(result)


# This code loads a pretrained DistilBERT sentiment classifier, runs it on Apple Silicon via MPS, and predicts whether a sentence expresses positive or negative sentiment.

# In[2]:


result = classifier("I love going to carlifonia for holidays")
print(result)


# In[ ]:




