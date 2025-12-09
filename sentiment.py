from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
import nltk
import re

nltk.download('punkt')

# Load model
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# Define sentiment classes manually (required for Cardiff NLP)
labels = ["NEGATIVE", "NEUTRAL", "POSITIVE"]

emoji_map = {
    "NEGATIVE": "😠",
    "NEUTRAL": "😐",
    "POSITIVE": "😄"
}

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def analyze_sentiment(text):
    text = clean_text(text)
    sentences = nltk.sent_tokenize(text)

    sentiment_totals = {label: 0.0 for label in labels}
    sentence_results = []

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits[0].numpy()
        probs = softmax(logits)

        for i, label in enumerate(labels):
            sentiment_totals[label] += float(probs[i])

        max_idx = probs.argmax()
        label = labels[max_idx]
        score = round(float(probs[max_idx]), 3)

        sentence_results.append({
            "sentence": sentence,
            "label": label,
            "score": score,
            "emoji": emoji_map.get(label, "")
        })

    sentence_count = len(sentences)
    normalized_distribution = {
        label: round(sentiment_totals[label] / sentence_count, 3)
        for label in labels
    }

    final_label = max(normalized_distribution, key=normalized_distribution.get)
    final_score = normalized_distribution[final_label]

    return {
        "overall_sentiment": final_label,
        "emoji": emoji_map.get(final_label, ""),
        "score": final_score,
        "distribution": normalized_distribution,
        "sentence_level": sentence_results
    }
