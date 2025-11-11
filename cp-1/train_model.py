import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib, os

# --- Step 1: Training data (you can expand later) ---
data = pd.DataFrame({
    'text': [
        'Win a free iPhone now!',
        'Congratulations, you have won a lottery!',
        'Claim your prize by clicking this link',
        'Important meeting at 10am tomorrow',
        'Hey, are you available for lunch?',
        'Your invoice is attached',
        'Earn money fast online now',
        'Exclusive offer just for you, buy now!',
        'Let’s catch up soon',
        'Project deadline extended to next week'
    ],
    'label': ['spam','spam','spam','ham','ham','ham','spam','spam','ham','ham']
})

# --- Step 2: Split data ---
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# --- Step 3: Create and train model ---
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('nb', MultinomialNB())
])
model.fit(X_train, y_train)

# --- Step 4: Save model ---
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/spam_model.pkl")

print("✅ Spam Detection Model trained and saved successfully at model/spam_model.pkl")
