import streamlit as st
import requests

# Set up the Streamlit page configuration
st.set_page_config(page_title="Mental Health Chatbot", page_icon=":robot_face:")

# Define the Flask API endpoint
FLASK_API_URL = "http://localhost:8080/get"

# Predefined questions
predefined_questions = [
    "How are you feeling today?",
    "What brings you here today?",
    "Can you describe any specific symptoms or issues you're experiencing?",
    "Have you been diagnosed with any mental health conditions in the past?",
    "Are you currently taking any medications or treatments for mental health?",
    "Do you have any concerns or questions about your mental health?"
]

# Create a chat function to handle sending and receiving messages
def chat_with_bot(user_answers):
    """
    Sends user answers to the Flask API and returns the response.

    Parameters:
    user_answers (list): A list of user answers.

    Returns:
    str: The response from the Flask API.
    """
    response = requests.post(FLASK_API_URL, json={"answers": user_answers})
    return response.text

# Initialize session state variables
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = [""] * len(predefined_questions)

st.title("SycoDoca")
st.title("Mental Health Chatbot")

# Display questions and input boxes for answers
for i, question in enumerate(predefined_questions):
    st.write(question)
    st.session_state["user_answers"][i] = st.text_input(f"Your answer for question {i+1}", value=st.session_state["user_answers"][i])

# Send button
if st.button("Send"):
    # Get user answers
    user_answers = st.session_state["user_answers"]
    # Get bot response
    bot_response = chat_with_bot(user_answers)
    # Display bot response
    st.write("Bot:", bot_response)

# Add copyright text
st.markdown(
    """
<div style="position: fixed; bottom: 10px; left: 50%; transform: translateX(-50%); padding: 10px; font-size: 12px; color: #666;">
    Designed and Developed by Pahanmi (PVT) Ltd
</div>
""",
    unsafe_allow_html=True
)

# Add some styling
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .stTextInput > div > input {
        padding: 12px;
        font-size: 16px;
        border-radius: 10px;
        border: 2px solid #ccc;
        background-color: #f7f7f7;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stButton>button:before {
        content: "\\1F4AC"; /* Add a speech bubble icon before the button text */
        margin-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
