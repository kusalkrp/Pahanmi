import streamlit as st
from streamlit_chat import message
import time

# Set up the Streamlit page configuration
st.set_page_config(page_title="Mental Health Chatbot", page_icon=":robot_face:")

# Predefined questions and answers
predefined_conversation = [
    {"question": "What else does she do often?", "answer": "She searches her phone everywhere while holding her phone."},
    {"question": "How does she react when you are being nice to her?", "answer": "She storms at me when I’m being nice to her."},
    {"question": "Does she ask you any specific types of questions?", "answer": "She constantly asks stupid hypothetical questions."}
]

final_response = "This is typical women!!"

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "question_index" not in st.session_state:
    st.session_state["question_index"] = 0
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Function to handle user input submission
def submit_user_input():
    user_input = st.session_state["user_input"]
    if user_input:
        st.session_state["messages"].append({"sender": "user", "content": user_input})
        st.session_state["user_input"] = ""
        st.session_state["question_index"] += 1
        if st.session_state["question_index"] == 1:
            first_question = "What else does she do often?"
            st.session_state["messages"].append({"sender": "bot", "content": first_question})
        elif st.session_state["question_index"] < len(predefined_conversation) + 1:
            next_question = predefined_conversation[st.session_state["question_index"] - 1]["question"]
            st.session_state["messages"].append({"sender": "bot", "content": next_question})
        else:
            # Display final bot response after a delay
            time.sleep(1.5)
            styled_final_response = f"<div class='highlight'>{final_response}</div>"
            st.session_state["messages"].append({"sender": "bot", "content": styled_final_response})

st.markdown("# SycoDoca By Pahanmi e-University")
st.markdown("## Mental Health Chatbot")

# Display existing messages
for i, msg in enumerate(st.session_state["messages"]):
    key = f"{msg['sender']}_{i}"
    if msg["sender"] == "user":
        message(msg["content"], is_user=True, key=key)
    else:
        if "highlight" in msg["content"]:
            st.markdown(f"""<div class='highlight'>{msg['content'].replace("<div class='highlight'>", "").replace("</div>", "")}</div>""", unsafe_allow_html=True)
        else:
            message(msg["content"], is_user=False, key=key)

# Text input for user response
if st.session_state["question_index"] < len(predefined_conversation) + 1:
    st.text_input("Tell me:", key="user_input", on_change=submit_user_input)
else:
    # Add some space before the button
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("Start again"):
        st.session_state["messages"] = []
        st.session_state["question_index"] = 0
        st.session_state["user_input"] = ""

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
    .stTitle {
        font-size: 15px;
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
        font-weight:bold;
        border-radius: 10px;
        background-color: #27ce4b;
        color: black;
        border: none;
        cursor: pointer;
        margin-top: 20px; /* Add margin-top to create space */
    }
    .stButton>button:hover {
        background-color: #27ce4b;
    }
    .stButton>button:before {
        content: "\\1F4AC"; /* Add a speech bubble icon before the button text */
        margin-right: 8px;
    }
    .highlight {
        font-weight:bold;
        font-size: 20px;
        background-color: #d3d3d3;
        color: black;
        padding: 8px;
        border-radius: 8px;
       
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin: 10px 0;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
