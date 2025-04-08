import streamlit as st
from utils import load_user_data, save_user_data, register, login
from sentiment import analyze_sentiment
from chatbot import get_chat_response
from datetime import datetime

st.set_page_config(page_title="AI Mental Health Companion", layout="centered")

phq9_questions = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself — or that you are a failure",
    "Trouble concentrating on things",
    "Moving or speaking slowly or being fidgety",
    "Thoughts that you would be better off dead or of hurting yourself"
]

gad7_questions = [
    "Feeling nervous, anxious or on edge",
    "Not being able to stop or control worrying",
    "Worrying too much about different things",
    "Trouble relaxing",
    "Being so restless that it is hard to sit still",
    "Becoming easily annoyed or irritable",
    "Feeling afraid as if something awful might happen"
]

st.title("🧠 AI Mental Health Companion")
user_data = load_user_data()

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])
username = None

if menu == "Register":
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Register"):
        if register(new_user, new_pass):
            st.success("Account created! Please log in.")
        else:
            st.error("Username already exists.")

elif menu == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success(f"Welcome back, {username}")
            user = user_data[username]

            if not user["phq9"]:
                st.subheader("📝 PHQ-9 & GAD-7 Questionnaire")
                st.markdown("Answer each question (0=None, 3=Nearly Every Day)")
                phq_scores = [st.slider(q, 0, 3, 0) for q in phq9_questions]
                gad_scores = [st.slider(q, 0, 3, 0) for q in gad7_questions]
                if st.button("Submit Questionnaire"):
                    user_data[username]["phq9"] = phq_scores
                    user_data[username]["gad7"] = gad_scores
                    save_user_data(user_data)
                    st.success("Responses saved. Proceed to dashboard.")
            else:
                tab = st.selectbox("📋 Dashboard", ["My Journal", "Mood Calendar", "Chatbot"])
                if tab == "My Journal":
                    st.subheader("📒 Daily Journal")
                    entry = st.text_area("How are you feeling today?")
                    if st.button("Save Entry"):
                        label, score = analyze_sentiment(entry)
                        user["journal"].append({
                            "date": str(datetime.now()),
                            "text": entry,
                            "sentiment": label,
                            "score": score
                        })
                        save_user_data(user_data)
                        st.success(f"Journal saved with sentiment: {label}")
                elif tab == "Mood Calendar":
                    st.subheader("📆 Mood Calendar")
                    for j in user["journal"][-7:]:
                        st.write(f"🗓 {j['date']}: {j['sentiment']} ({j['score']:.2f})")
                elif tab == "Chatbot":
                    st.subheader("💬 24/7 Support Chatbot")
                    message = st.text_input("You:", key="chat_input")
                    if st.button("Send"):
                        response = get_chat_response(username, message)
                        st.text_area("AI:", value=response, height=100)
                        user["chat"].append({"user": message, "bot": response})
                        save_user_data(user_data)
        else:
            st.error("Incorrect username or password.")
