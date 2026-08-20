import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from tools import currency_converter


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

HF_TOKEN = (
    os.getenv("HF_TOKEN")
    or os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

if not HF_TOKEN:
    raise ValueError(
        "Hugging Face API token not found. "
        "Set HF_TOKEN in environment variables."
    )

HF_TOKEN = HF_TOKEN.strip()


# ==========================================
# HUGGING FACE CLIENT
# ==========================================

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN,
)


# ==========================================
# MODEL
# ==========================================

MODEL = "HuggingFaceH4/zephyr-7b-beta"


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are an AI currency conversion assistant.

You help users with currency-related questions and conversions.

Rules:

1. For actual currency conversion requests, use the
   currency_converter tool.

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
CHF = Swiss Franc
CNY = Chinese Yuan
SGD = Singapore Dollar

4. If the user gives a currency name instead of a code,
   convert it to the correct ISO code.

5. After a conversion, clearly show:

Original amount
Original currency
Converted amount
Target currency
Exchange rate
Rate date

6. For simple questions such as:
   "What is the currency of Japan?"
   answer directly and concisely.

7. Keep responses simple and concise.
"""


# ==========================================
# TOOL HELPER
# ==========================================

def run_currency_tool(arguments):
    """
    Executes the currency converter tool.
    """

    try:
        return currency_converter.invoke(arguments)
    except AttributeError:
        return currency_converter(**arguments)


# ==========================================
# ASK AGENT
# ==========================================

def ask_currency_agent(user_input: str) -> str:

    if not user_input or not user_input.strip():
        return "Please enter a question."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_input.strip(),
        },
    ]

    response = client.chat_completion(
        messages=messages,
        model=MODEL,
        max_tokens=512,
        temperature=0.1,
    )

    return response.choices[0].message.content


# ==========================================
# LOCAL TEST
# ==========================================

if __name__ == "__main__":

    user_input = input("Enter your question: ")

    result = ask_currency_agent(user_input)

    print("\nAI Response:")
    print(result)
