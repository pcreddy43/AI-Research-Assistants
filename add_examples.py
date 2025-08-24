from dotenv import load_dotenv
load_dotenv()

import os
print("API KEY:", os.environ.get("LANGCHAIN_API_KEY"))
from langsmith import Client

client = Client()

dataset_name = "agentic-eval"  # Change to your dataset name if different

examples = [
    {
        "inputs": {"question": "What is agentic AI?"},
        "outputs": {"answer": "Agentic AI refers to artificial intelligence systems that act as agents, making decisions and taking actions autonomously."}
    },
    {
        "inputs": {"question": "List 3 features of agentic AI."},
        "outputs": {"answer": "1. Autonomy 2. Goal-directed behavior 3. Ability to interact with the environment"}
    }
]

for ex in examples:
    client.create_example(
        inputs=ex["inputs"],
        outputs=ex["outputs"],
        dataset_name=dataset_name
    )

print("Examples added to dataset:", dataset_name)
