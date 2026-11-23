"""CodeAlpha AI Internship - Task 2: Chatbot for FAQs
Uses NLTK for text preprocessing and TF-IDF + cosine similarity to match questions.
Run in terminal:  python chatbot.py
"""
import json
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data (only downloads the first time)
for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet"]:
    nltk.download(pkg, quiet=True)

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()
GREETINGS = {"hi", "hello", "hey", "hii", "hola"}
EXITS = {"quit", "exit", "bye", "goodbye"}


def preprocess(text: str) -> str:
    """Lowercase -> remove punctuation -> tokenize -> remove stopwords -> lemmatize."""
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    tokens = [LEMMATIZER.lemmatize(t) for t in tokens if t not in STOP_WORDS]
    return " ".join(tokens)


class FAQChatbot:
    def __init__(self, faq_file="faqs.json", threshold=0.2):
        with open(faq_file, encoding="utf-8") as f:
            self.faqs = json.load(f)
        self.threshold = threshold
        self.questions = [preprocess(item["question"]) for item in self.faqs]
        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = self.vectorizer.fit_transform(self.questions)

    def get_response(self, user_input: str) -> str:
        cleaned = user_input.lower().strip()
        if cleaned in GREETINGS:
            return "Hello! Ask me anything about the internship."
        if cleaned in EXITS:
            return "Goodbye! Have a great day."

        processed = preprocess(user_input)
        if not processed:
            return "Please type a question."

        user_vec = self.vectorizer.transform([processed])
        scores = cosine_similarity(user_vec, self.faq_vectors)[0]
        best = scores.argmax()

        if scores[best] < self.threshold:
            return "Sorry, I couldn't find an answer. Try rephrasing, or email services@codealpha.tech."
        return self.faqs[best]["answer"]


def main():
    bot = FAQChatbot()
    print("FAQ Chatbot ready! Type 'quit' to exit.\n")
    while True:
        user = input("You: ")
        reply = bot.get_response(user)
        print("Bot:", reply, "\n")
        if user.lower().strip() in EXITS:
            break


if __name__ == "__main__":
    main()
