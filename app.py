import streamlit as st
import pickle
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()
    for i  in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)


# Load your pre-trained model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title("Email/SMS Spam Classifier")
input_sms = st.text_input("Enter the message")

if st.button('Predict'):
    # Preprocess
    transform_sms = transform_text(input_sms)
    # Vectorize
    vector_input = tfidf.transform([transform_sms])
    # Predict 
    result = model.predict(vector_input)[0]
    # Display result
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")