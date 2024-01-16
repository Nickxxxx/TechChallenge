import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class EmotionClassifier:
    def __init__(self):
        # Load the tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained("badmatr11x/roberta-base-emotions-detection-from-text")
        self.model = AutoModelForSequenceClassification.from_pretrained("badmatr11x/roberta-base-emotions-detection-from-text")

    def predict_emotion(self, text):
        # Tokenize the input text and convert to tensor
        inputs = self.tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")

        # Predict
        with torch.no_grad():
            logits = self.model(**inputs).logits

        # Convert logits to probabilities
        probabilities = torch.nn.functional.softmax(logits, dim=1)

        # Convert probabilities to percentages
        percentages = probabilities[0].tolist()  # Convert the first (and only) batch of probabilities to a list

        # Emotion labels (adjust based on the model's specific output)
        labels = ["joy", "anger", "sadness", "disgust", "surprise", "fear", "neutral"]

        # Create a dictionary of emotion: percentage
        emotion_probabilities = {labels[i]: round(percent * 100, 2) for i, percent in enumerate(percentages)}

        return emotion_probabilities
