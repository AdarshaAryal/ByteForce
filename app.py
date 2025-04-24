import os

from openai import AzureOpenAI

# In production inject environment variables from the web app configuration
# Not hard code the values in the code
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://byteforceopenai.openai.azure.com/"
os.environ["AZURE_OPENAI_KEY"] = (
    "4AQKFc9hRCk6PR85SQyYYLLLc7sXYJCBjr7fNnoTDGOfIKStmAFyJQQJ99BDACmepeSXJ3w3AAABACOGeD71"
)
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "o3-mini"


client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-03-01-preview",
)

prompt = "<to_be_filled_up>"

response = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that helps people who may have mental health issues with their financial issues",
        },
        {"role": "user", "content": prompt},
    ],
    max_completion_tokens=5000,
)

print(response.model_dump_json(indent=2))
