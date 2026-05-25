from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)


def analyze_sentiment(text):

    result = classifier(text)

    label = result[0]['label']
    score = result[0]['score']

    return label, score
