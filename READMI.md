# 💱 AI Currency Converter

An AI-powered currency conversion application built using
LangChain, Hugging Face, Python, Streamlit, and the Frankfurter API.

The application uses a LangChain agent with a custom currency
conversion tool to fetch the latest available exchange rate
and calculate the converted amount.

## 🚀 Features

- Convert currencies using natural language
- Live exchange rates using Frankfurter API
- LangChain tool-based agent
- Hugging Face LLM integration
- Streamlit web interface
- Supports major currencies such as USD, EUR, INR, GBP, JPY, CAD and AUD
- Error handling for invalid currency pairs
- Displays exchange rate and rate date

## 🛠️ Technologies Used

- Python
- LangChain
- LangGraph
- Hugging Face
- Streamlit
- Requests
- Frankfurter API
- python-dotenv

## 📁 Project Structure

```text
currency/
│
├── agents.py
├── tools.py
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env


# HOW ITS WORK
User
  ↓
Streamlit UI
  ↓
LangChain Agent
  ↓
Hugging Face LLM
  ↓
Currency Converter Tool
  ↓
Frankfurter API
  ↓
Exchange Rate
  ↓
Converted Amount  


#PROJECT ARCHATECTURE

                 USER
                   │
          ┌────────┴────────┐
          │                 │
    Manual Converter      AI Chat
          │                 │
          │            LangChain Agent
          │                 │
          │          Hugging Face Model
          │                 │
          └────────┬────────┘
                   │
          Currency Converter
                 Tool
                   │
          Frankfurter API
                   │
          Current Exchange Rate