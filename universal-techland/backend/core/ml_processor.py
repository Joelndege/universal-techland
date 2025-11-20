import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .utils import clean_text
from django.conf import settings

# Categories and their severity levels
CATEGORIES = {
    'crime': 4,
    'accident': 3,
    'weather': 2,
    'disaster': 5,
    'civil_unrest': 4,
    'other': 1,
}

# Sample training data (in production, this would be a trained model)
SAMPLE_DATA = [
    ("Police arrest suspect in robbery", "crime"),
    ("Car crash on highway causes traffic", "accident"),
    ("Heavy rain expected tomorrow", "weather"),
    ("Earthquake hits coastal area", "disaster"),
    ("Protests turn violent in city center", "civil_unrest"),
    ("New restaurant opens downtown", "other"),
    ("Murder investigation ongoing", "crime"),
    ("Flood warning issued", "disaster"),
    ("Riots break out after game", "civil_unrest"),
    ("Sunny weather forecast", "weather"),
]

def train_model():
    """Train a simple ML model for incident classification."""
    texts = [clean_text(text) for text, _ in SAMPLE_DATA]
    labels = [label for _, label in SAMPLE_DATA]
    
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(texts)
    
    model = LogisticRegression(random_state=42)
    model.fit(X, labels)
    
    return model, vectorizer

def classify_incident(text):
    """Classify incident text and return category and severity."""
    # Load or train model
    model_path = os.path.join(settings.BASE_DIR, 'ml_model.pkl')
    vectorizer_path = os.path.join(settings.BASE_DIR, 'vectorizer.pkl')
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
    else:
        model, vectorizer = train_model()
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
    
    # Clean and vectorize text
    cleaned_text = clean_text(text)
    X = vectorizer.transform([cleaned_text])
    
    # Predict category
    prediction = model.predict(X)[0]
    
    # Get severity
    severity = CATEGORIES.get(prediction, 1)
    
    return prediction, severity
