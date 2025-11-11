# 📧 Spam Email Detection System

This project detects whether an email is **Spam or Not Spam** using **Machine Learning** and **Natural Language Processing (NLP)**.  
It analyzes the text content of emails and classifies them using a trained ML model.

---

## 🚀 Features
- Classifies emails as **Spam** or **Not Spam**
- Uses **TF-IDF Vectorization** for text representation
- Built using **Naïve Bayes Classifier**
- Simple and interactive web interface (Flask/Streamlit)
- Trained on a public spam email dataset

---

## 🧠 How It Works
1. The email text is preprocessed (removing punctuation, stopwords, and converting to lowercase).  
2. Text is converted into numeric vectors using **TF-IDF**.  
3. The model is trained using **Multinomial Naïve Bayes**.  
4. When a user inputs an email, the system predicts whether it's *spam* or *not spam*.

---

## 🧰 Tech Stack
- **Python 3**
- **Pandas**, **NumPy**
- **scikit-learn**
- **NLTK**
- **Flask** or **Streamlit** (for UI)

---

## 📦 Installation & Usage

### 1️⃣ Clone the repository

Example Output

Input:

“Congratulations! You have won a free iPhone. Click the link below to claim your prize!”

Prediction:

🟥 Spam

Input:

“Hey, can we reschedule our meeting for tomorrow?”

Prediction:

🟩 Not Spam

```bash
git clone https://github.com/your-username/spam-email-detection.git
cd spam-email-detection
