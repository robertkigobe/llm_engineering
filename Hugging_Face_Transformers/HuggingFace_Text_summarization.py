#!/usr/bin/env python
# coding: utf-8

# 	This code loads a pretrained AI summarization model and uses it to generate a concise summary of a long article. Here’s a clear, step-by-step explanation of what’s happening.
#    		•	torch → the deep learning framework running the model
# 	•	transformers → the library from Hugging Face that provides pretrained NLP models
# 	•	AutoModelForSeq2SeqLM → loads a sequence-to-sequence language model (input text → output text)
# 	•	AutoTokenizer → converts text into tokens the model understands
# 	•	pipeline → a high-level API that simplifies inference
# 
# 	•	This is a DistilBART model fine-tuned for text summarization
# 	•	Trained on the CNN/DailyMail news summarization dataset
# 	•	Designed to take long text and output a short summary
# 
# 
# 	•	Converts your article into numerical tokens
# 	•	Handles sentence splitting, padding, and truncation automatically
# 
# 	•	Loads the pretrained summarization model
# 	•	.to("mps") moves it to Apple Silicon GPU using Metal Performance Shaders
# 		(great for M1/M2/M3 Macs via Apple hardware)
# 
# 	•	max_length=500 → summary will not exceed 500 tokens
# 	•	min_length=25 → ensures the summary isn’t too short
# 	•	do_sample=False → uses deterministic decoding (stable, factual output)
# 
# 	This code takes a long article and automatically produces a clear, condensed summary using a pretrained AI model, running efficiently on a Mac GPU.

# In[6]:


import torch
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

model_id ="sshleifer/distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to("mps")
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device="mps")
text = ("""The Connected Family: Using Mobile Phones with Wisdom, Respect, and Safety"
Author: Robert Kigobe
There is something quietly symbolic about the way a phone lights up in a dark room. It pulls every eye toward it instantly, drawing attention away from whoever was there before it. For many of our families here in Boston and across the diaspora, that small glowing screen has become one of the most powerful, and least examined, forces shaping our homes. As Ugandan Catholic families who have sacrificed enormously to build life in a foreign land, we owe it to ourselves and our children to be intentional about how this technology serves us, rather than silently governing us.
This is not an article about fear. It is about wisdom, the same wisdom our parents exercised about what entered their homes, now applied to the digital world that has moved in with us without ever knocking on the door.

The Phone Is Not the Problem, The Absence of Boundaries Is
Mobile phones are genuinely remarkable tools. They connect us to family in Kampala at midnight, help our children access world-class educational resources, navigate unfamiliar bus routes, manage finances, and keep us anchored to community and faith through Scripture apps, podcasts, and online Mass. For immigrant families especially, the smartphone has been a lifeline.
But a lifeline can become a leash. When phones appear at every meal, in every bedroom, and inside every conversation, they stop being tools and become competitors, for our spouses' attention, for presence with our children, for the quiet morning moments that belong to God. As families rooted in the faith of the Uganda Martyrs, we are called to bring the same intentionality to our digital lives that we bring to our prayer lives.

Protecting Your Family from Outside Bad Actors
The dangers in the digital world are real and deserve direct conversation in our homes.
Platforms designed for entertainment, TikTok, Snapchat, Instagram, and even online gaming, contain private messaging features that predators exploit to contact children directly. These individuals are patient and methodical, befriending children over weeks before introducing harmful content or requests. The most effective protection is not a single rule but an ongoing relationship: create a home culture where children know they will never be in trouble for bringing an uncomfortable online experience to a parent. Keep devices in shared family spaces, and make "who are you talking to?" a normal dinner conversation rather than an accusation.
Our immigrant community is also a specific target of financial scams delivered through WhatsApp, Facebook Messenger, and text messages. These include fake immigration attorneys offering green card shortcuts, fraudulent job offers, and urgent messages impersonating family members in distress. The firm rule is this, if anyone contacts you unexpectedly requesting money, documents, or personal information, even claiming to know you, verify through a separate direct phone call before taking any action. No legitimate immigration attorney solicits clients through a WhatsApp voice note.
On privacy, many of us share generously and joyfully on social media, which is a beautiful instinct. But school uniforms visible in photos, home addresses in the background of videos, and travel announcements that reveal when your home is empty create a detailed profile that can be exploited. Take ten minutes this week to set your Facebook and Instagram accounts to "Friends Only" or "Private," and think carefully before posting details about your children's daily routines.

""")
result = summarizer(text, max_length=500, min_length=25, do_sample=False)
print(result[0]['summary_text'])


# This code loads a pretrained DistilBERT sentiment classifier, runs it on Apple Silicon via MPS, and predicts whether a sentence expresses positive or negative sentiment.
