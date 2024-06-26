from huggingface_hub import InferenceClient
import json

# Your Hugging Face API token
HF_TOKEN = "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"

# Repository ID for the model you want to use
repo_id = "meta-llama/Meta-Llama-3-70B-Instruct"

# Initialize the InferenceClient with the token and model
llm_client = InferenceClient(
    model=repo_id,
    token=HF_TOKEN,  # Adding the token here for authentication
    timeout=120,
)

def call_llm(inference_client: InferenceClient, prompt: str):
    response = inference_client.post(
        json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200},
            "task": "text-generation",
        },
    )
    return json.loads(response.decode())[0]["generated_text"]

response = call_llm(llm_client, "create a python code to print 1 to 5")
print(response)
