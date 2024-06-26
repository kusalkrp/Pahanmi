from flask import Flask, request, jsonify
from langchain.chains import RetrievalQA
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hugging_face_embeddings
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from dotenv import load_dotenv
import os
from src.prompt import prompt_template

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')

embeddings = download_hugging_face_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index_name = "mental-chatbot"
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

llm = CTransformers(
    model="model/llama-2-7b-chat.ggmlv3.q8_0.bin",
    model_type="llama",
    config={'max_new_tokens': 1024, 'temperature': 0.2}  # Reduce max_new_tokens
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

def truncate_text(text, max_length=256):
    """Truncate the text to a maximum number of tokens."""
    tokens = text.split()
    return ' '.join(tokens[:max_length])

@app.route("/get", methods=["POST"])
def chat():
    user_answers = request.json.get("answers")
    response = generate_response(user_answers)
    return jsonify({"response": response})

def generate_response(user_answers):
    """
    Generates a response from the bot based on the user's answers.

    Args:
        user_answers (list): A list of user's answers.

    Returns:
        str: The generated response from the bot.
    """
    # Concatenate user answers
    user_input = " ".join(user_answers)
    # Truncate the input to ensure it doesn't exceed the maximum length
    user_input = truncate_text(user_input, max_length=200)
    # Generate bot response using RAG model
    result = qa({"query": user_input})
    return truncate_text(result["result"], max_length=300)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
