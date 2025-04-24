import os
from openai import AzureOpenAI

endpoint = "https://byteforceopenai.openai.azure.com/"
model_name = "gpt-4"
deployment = "gpt-4"

subscription_key = "<your-api-key>"
with open("api_key.txt", "r") as f:
    subscription_key = f.read().strip()
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def get_response(input):
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are talking through a user on a banking app who is on the verge of making a potential harmful purchase. Talk them through the emotions they're feelings. Entries marked by 'Bot' are your previous responses. Keep your responses short and sweet. Encourage them to distract themselves from making the purchase.",
        },
        {
            "role": "user",
            "content": input,
        }
    ],
    max_tokens=4096,
    model=deployment
)
    return response.choices[0].message.content.strip()