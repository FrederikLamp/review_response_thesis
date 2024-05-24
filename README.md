This repository holds example python code from the scripts used to fine-tune pretrained transformer models for both text 
classification and text generation tasks based on Danish review data collected from Trustpilot.

The TP_scrape.py and concatenate_reviews.py was used in data collection, and the notebooks were used in the text classification, 
text generation, and dataset descriptive statistics tasks, respectively.


Packages & versions I have used during this project:

Python       3.10.6
transformers 4.41.0.dev0 (source)
torch        2.2.2

requests     2.31.0
Scrapy       2.11.1

pandas       1.5.3
scikit-learn 1.2.1
nltk         3.8.1
accelerate   0.30.1
matplotlib   3.6.0
