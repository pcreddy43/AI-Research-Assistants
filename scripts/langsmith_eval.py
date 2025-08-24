import os
from dotenv import load_dotenv
load_dotenv()
from langchain.smith import RunEvalConfig, run_on_dataset
from langsmith import Client
from langchain_openai import ChatOpenAI

# Make sure your .env has LANGCHAIN_API_KEY and LANGCHAIN_TRACING_V2=true

# Example: Evaluate a simple chain on a dataset in LangSmith

def main():
    # Set up your chain (replace with your actual chain)
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    def chain(input):
        # If input is a dict, extract the question
        if isinstance(input, dict):
            input = input.get("question", "")
        return llm.invoke(input)

    # Configure evaluation
    eval_config = RunEvalConfig(
        evaluators=["qa"],  # or "criteria", "cot_qa", etc.
    )

    # Run on a dataset (replace with your dataset name or id)
    dataset_name = os.environ.get("LANGSMITH_DATASET", "my-dataset")
    client = Client()
    run_on_dataset(
        dataset_name=dataset_name,
        llm_or_chain_factory=chain,
        evaluation=eval_config,
        concurrency_level=2,
        client=client,
    )

if __name__ == "__main__":
    main()
