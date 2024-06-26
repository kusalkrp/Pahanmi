import streamlit as st
import requests
from streamlit_chat import message

# Set up the Streamlit page configuration
st.set_page_config(page_title="Mental Health Chatbot", page_icon=":robot_face:")

# Define the Flask API endpoint
FLASK_API_URL = "http://localhost:8080/get"

# Predefined questions
predefined_questions = [
    "Can you describe any recent changes in your mood or emotions? Have there been times when you felt extremely sad, overly happy, or irritable for extended periods?",
    "How has your energy level fluctuated over the past few weeks? Do you often feel exhausted or unusually energetic without clear reasons?",
    "How often do you feel anxious or worried, and what typically triggers these feelings? Do these feelings interfere with your daily activities?",
    #"How would you describe your sleep patterns lately? Have you experienced difficulties falling asleep, staying asleep, or sleeping too much? How does this affect your daytime functioning?",
   # "Have you noticed any changes in your appetite or eating habits? Are you eating more or less than usual, and how do you feel about your body weight and shape?",
    #"How do you generally feel in social situations? Have you been avoiding social interactions, and if so, why? Do you feel overly shy or fear being judged by others?",
    #"Can you describe any impulsive behaviors you've noticed in yourself, such as acting without thinking or engaging in risky activities? How often do these behaviors occur, and what are the typical outcomes?",
    #"Have you experienced moments of feeling disconnected from reality or observing yourself from outside your body? Do you have any gaps in your memory or trouble recalling specific events?",
   # "Are you dealing with any physical symptoms like pain, fatigue, or digestive issues that don't have a clear medical explanation? How do these symptoms impact your daily life?",
    #"Have you gone through any traumatic events that still affect you? How do these experiences manifest in your life, such as through flashbacks, nightmares, or intense emotional distress?",
]

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = []
if "question_index" not in st.session_state:
    st.session_state["question_index"] = 0
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Create a chat function to handle sending and receiving messages
def chat_with_bot(user_answers):
    response = requests.post(FLASK_API_URL, json={"answers": user_answers})
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return "Error: Unable to get response from the bot."

st.title("SycoDoca")
st.title("Mental Health Chatbot")

# Function to handle user input submission
def submit_user_input():
    user_input = st.session_state["user_input"]
    if user_input:
        st.session_state["messages"].append({"sender": "user", "content": user_input})
        st.session_state["user_answers"].append(user_input)
        st.session_state["user_input"] = ""
        st.session_state["question_index"] += 1
        if st.session_state["question_index"] < len(predefined_questions):
            next_question = predefined_questions[st.session_state["question_index"]]
            st.session_state["messages"].append({"sender": "bot", "content": next_question})
        else:
            # Generate the final bot response
            bot_response = chat_with_bot(st.session_state["user_answers"])
            st.session_state["messages"].append({"sender": "bot", "content": bot_response})

# Display existing messages
for i, msg in enumerate(st.session_state["messages"]):
    key = f"{msg['sender']}_{i}"
    if msg["sender"] == "user":
        message(msg["content"], is_user=True, key=key)
    else:
        message(msg["content"], is_user=False, key=key)

# Ask the first question initially
if st.session_state["question_index"] == 0 and not st.session_state["messages"]:
    first_question = predefined_questions[0]
    st.session_state["messages"].append({"sender": "bot", "content": first_question})

# Text input for user response
if st.session_state["question_index"] < len(predefined_questions):
    st.text_input("Your answer:", key="user_input", on_change=submit_user_input)
else:
    if st.button("Start a new conversation"):
        st.session_state["messages"] = []
        st.session_state["user_answers"] = []
        st.session_state["question_index"] = 0
        st.session_state["user_input"] = ""
        first_question = predefined_questions[0]
        st.session_state["messages"].append({"sender": "bot", "content": first_question})

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
        cursor: pointer.
    }
    .stButton>button:hover {
        background-color: #45a049.
    }
    .stButton>button:before {
        content: "\\1F4AC"; /* Add a speech bubble icon before the button text */
        margin-right: 8px.
    }
    </style>
    """,
    unsafe_allow_html=True,
)
