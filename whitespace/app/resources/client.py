import os
from enum import Enum

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()


class OpenAIModel(Enum):
    # GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo"


def get_openai_client(model: str, temperature: float):
    return AzureChatOpenAI(
        azure_deployment="GPT4O-NORWAY" if model == "gpt-4o" else model,
        api_version="2023-03-15-preview",  # or your api version
        api_key=os.environ.get("AZURE_OPENAI_KEY"),
        azure_endpoint="https://bettersg-openai-norwayeast-prod.openai.azure.com/",
        temperature=temperature,
        max_tokens=2048,
        max_retries=2,
    )
