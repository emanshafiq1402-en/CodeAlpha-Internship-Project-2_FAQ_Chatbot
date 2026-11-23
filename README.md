# CodeAlpha_FAQ_Chatbot

FAQ chatbot built for the CodeAlpha AI Internship (Task 2).

## How it works
1. FAQs are stored in `faqs.json`.
2. Text is cleaned with NLTK (lowercase, remove punctuation, tokenize, remove stopwords, lemmatize).
3. TF-IDF converts text to numbers.
4. Cosine similarity finds the most similar FAQ.
5. The matching answer is shown. If nothing is similar enough, the bot says it could not find an answer.

## Setup
```
pip install -r requirements.txt
```

## Run (terminal)
```
python chatbot.py
```

## Run (chat UI)
```
streamlit run app.py
```

## Tech
Python, NLTK, scikit-learn, Streamlit
