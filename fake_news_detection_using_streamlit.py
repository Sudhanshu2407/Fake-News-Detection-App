import streamlit as st
import pyttsx3
import pickle
from pathlib import Path
import re

# Load your model
model = pickle.load(open(r"C:\sudhanshu_projects\project-task-training-course\fake-news-prediction\fake_news_detection.pkl","rb"))  # Change the path to your saved model file

vectorizer = pickle.load(open(r"C:\sudhanshu_projects\project-task-training-course\fake-news-prediction\fake_news_vectorizer.pkl","rb"))

# Initialize text-to-speech engine
engine = pyttsx3.init()

# App title
st.set_page_config(page_title="Fake News Detector - NewsGuard", page_icon="📰")

# Pages
def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Choose Page", ["Signup", "Login", "News Check"])

    if choice == "Signup":
        signup()
    elif choice == "Login":
        login()
    elif choice == "News Check":
        news_check()

# Signup Page
def signup():
    st.title("Signup")
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        # Simple file-based storage (For demo purposes only, use a database in production)
        if not Path("users.txt").exists():
            Path("users.txt").touch()

        with open("users.txt", "a") as f:
            f.write(f"{username},{password}\n")
        st.success("Account created successfully! You can now log in.")

# Login Page
def login():
    st.title("Login")
    st.subheader("Enter your credentials")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if not Path("users.txt").exists():
            st.error("No users found, please sign up first.")
            return

        with open("users.txt", "r") as f:
            users = f.readlines()
            users = [user.strip().split(",") for user in users]

        if [username, password] in users:
            st.success("Login successful!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials, please try again.")

# News Check Page
def news_check():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in first.")
        return

    st.title("News Check")
    st.subheader("Enter the news details")

    author = st.text_input("Author Name")
    title = st.text_input("News Title")
    if st.button("Predict"):
        if author and title:
            news_text = f"{author} {title}"
            prediction = predict_news(news_text)

            if prediction == 0:
                st.success("This news is Real. You can read it without any fear.")
                speak("This news is Real. You can read it without any fear.")
            else:
                st.error("This news is Fake. Do not read it and beware of such news.")
                speak("This news is Fake. Do not read it and beware of such news.")
        else:
            st.error("Please enter both author name and news title.")

# Prediction function
def predict_news(text):
    # Clean and prepare the text (example)
    cleaned_text = re.sub('[^a-zA-Z]', ' ', text.lower())
    
    cleaned_text = vectorizer.transform([cleaned_text])
    # Prediction using the loaded model
    prediction = model.predict(cleaned_text)[0]
    return prediction

# Text-to-speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    main()

