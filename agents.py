import os

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.agents import create_agent

from tools import currency_converter


# Load environment variables
load_dotenv()


# Get Hugging Face API key
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HUGGINGFACEHUB_API_TOKEN not found in .env file"
    )


# Hugging Face model
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.1,
    max_new_tokens=512,
)


# Convert Hugging Face model into chat model
model = ChatHuggingFace(
    llm=llm
)


# Tools
tools = [
    currency_converter
]


# Create LangChain agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
You are an AI currency conversion assistant.

You help users convert currencies.

Rules:

1. Always use the currency_converter tool for
   currency conversion requests.

2. Never guess or invent exchange rates.

3. Use ISO currency codes.

Examples:

USD = US Dollar
EUR = Euro
INR = Indian Rupee
GBP = British Pound
JPY = Japanese Yen
CAD = Canadian Dollar
AUD = Australian Dollar

4. If the user gives a currency name instead of
   a currency code, convert it to the correct ISO code.

5. After using the tool, clearly show:

Original amount
Original currency
Converted amount
Target currency
Exchange rate
Rate date

6. Keep the answer simple and concise.
"""
)


def ask_currency_agent(user_input: str) -> str:

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    return response["messages"][-1].content


# Test the agent
if __name__ == "__main__":

    user_input = input(
        "Enter currency conversion: "
    )

    result = ask_currency_agent(user_input)

    print("\nAI Response:")
    print(result)