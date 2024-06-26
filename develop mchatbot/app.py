from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = '64802009f671c417e07c6b3f95333e7b'

# Initialize MongoDB connection
#client = MongoClient("mongodb+srv://kusalcoc1212:Kusal01@chat-history.bjnpiqq.mongodb.net/")
#db = client["M-chatbot"]
#collection = db["chat_history"]



load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

embeddings = download_hugging_face_embeddings()

# Function to check if a predefined question should be asked based on user input
predefined_questions = {
    "How are you feeling today?": "feeling",
    "What brings you here today?": "reason_visit",
    "Can you describe any specific symptoms or issues you're experiencing?": "symptoms",
    "Have you been diagnosed with any mental health conditions in the past?": "diagnosis_past",
    "Are you currently taking any medications or treatments for mental health?": "medications",
    "Do you have any concerns or questions about your mental health?": "concerns",
    "Have you experienced any recent life changes or stressful events?": "life_changes",
    "How would you rate your sleep quality recently?": "sleep_quality",
    "Are you currently seeing a therapist or counselor?": "therapy",
    "Do you have any preferences or specific topics you'd like to learn more about?": "topics_preference",
    "Have you ever attended any mental health workshops or programs before?": "workshops_attended",
    "Are you interested in learning about coping strategies or relaxation techniques?": "coping_strategies",
    "Do you have any questions about mental health treatments or therapies available?": "treatments_available",
    "Would you like information on support groups or community resources?": "support_groups",
    "How can we best assist you today?": "assistance_needed",

}
# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index_name = "mental-chatbot"

# If we already have an index we can load it like this
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

llm = CTransformers(
    model="model\llama-2-7b-chat.ggmlv3.q8_0.bin",
    model_type="llama",
    config={'max_new_tokens': 512, 'temperature': 0.2}
)

qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs={})

# Function to delete old chat records
#def delete_old_records():
    #oldest_record_time = datetime.utcnow() - timedelta(hours=24)
    #collection.delete_many({"timestamp": {"$lt": oldest_record_time}})

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg.strip()

    # Check if there's an ongoing session or create a new one
    if "current_session" not in session:
        session["current_session"] = []

    # Add user input to the current session
    session["current_session"].append({"user": input_text, "timestamp": datetime.utcnow()})

    # Initialize session variables
    if "conversation_state" not in session:
        session["conversation_state"] = "start"

    # End session and save chat history to MongoDB
    if input_text.lower() in ["end", "finish", "goodbye"]:
        session_record = {
            "timestamp": datetime.utcnow(),
            "conversation": session["current_session"]
        }
        #collection.insert_one(session_record)
        session.pop("current_session", None)
        session["conversation_state"] = "end"
        return "Goodbye! Have a great day."

    # Handle greetings
    if input_text.lower() in ["hello", "hi", "hey", "start", "begin"]:
        session["conversation_state"] = "feeling"
        return "How are you feeling today?"

    # Handle unexpected input
    else:
        # If the user's input doesn't match any predefined question or greeting, proceed with RetrievalQA
        print("User's main question: ", input_text)
        result = qa({"query": input_text})
        response = str(result["result"])

        # Add bot response to the current session
        session["current_session"].append({"bot": response, "timestamp": datetime.utcnow()})

        return response
    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)