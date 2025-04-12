from dotenv import dotenv_values
import os
from openai import AzureOpenAI

config = dotenv_values(".env")
client = AzureOpenAI(
    api_key=config["api_key"],
    azure_endpoint=config["endpoint"],
    api_version="2024-05-01-preview",
)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello, how are you?"},
    ],
)
print(completion.choices[0].message.content)
