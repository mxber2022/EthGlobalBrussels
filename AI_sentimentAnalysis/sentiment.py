import pandas as pd
from transformers import pipeline
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

df = pd.read_csv("feedback.csv")
df= df.sample(200)

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

nlp = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
texts = list(df.content.values)
results = nlp(texts)
for text, result, score in zip(texts, results, df.score.values):
    print("text: ", text)
    print("result: ", result)
    print("score: ", score)