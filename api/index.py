import os
import sys

# Root directory ko Python path me add karna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from mangum import Mangum

try:
    from tools import currency_converter
    from agents import ask_currency_agent
except Exception as e:
    print(f"Import Error: {e}")

app = FastAPI(
    title="AI Currency Converter",
    description="AI-powered currency converter using LangChain and Hugging Face"
)


class ConversionRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str


class AIRequest(BaseModel):
    message: str


@app.get("/api")
def home():
    return {
        "status": "success",
        "message": "AI Currency Converter API is running"
    }


@app.post("/api/convert")
def convert_currency(request: ConversionRequest):
    try:
        result = currency_converter.invoke({
            "amount": request.amount,
            "from_currency": request.from_currency,
            "to_currency": request.to_currency
        })
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/ask")
def ask_ai(request: AIRequest):
    try:
        result = ask_currency_agent(request.message)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}


@app.get("/", response_class=HTMLResponse)
def frontend():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Currency Converter</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; }
            h1 { text-align: center; }
            input, select, button { width: 100%; padding: 12px; margin: 8px 0; box-sizing: border-box; }
            button { cursor: pointer; font-size: 16px; background-color: #0070f3; color: white; border: none; border-radius: 6px; }
            .box { border: 1px solid #ddd; padding: 20px; margin-top: 20px; border-radius: 10px; }
            #result, #airesult { margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>💱 AI Currency Converter</h1>

        <div class="box">
            <h2>Currency Converter</h2>
            <input id="amount" type="number" value="100" min="0.01" placeholder="Amount">
            <select id="from_currency">
                <option>USD</option><option>EUR</option><option>INR</option>
                <option>GBP</option><option>JPY</option><option>CAD</option>
                <option>AUD</option><option>CHF</option><option>CNY</option><option>SGD</option>
            </select>
            <select id="to_currency">
                <option>INR</option><option>USD</option><option>EUR</option>
                <option>GBP</option><option>JPY</option><option>CAD</option>
                <option>AUD</option><option>CHF</option><option>CNY</option><option>SGD</option>
            </select>
            <button onclick="convertCurrency()">🔄 Convert</button>
            <div id="result"></div>
        </div>

        <div class="box">
            <h2>🤖 Ask AI</h2>
            <input id="question" placeholder="Example: Convert 500 USD to INR">
            <button onclick="askAI()">Ask AI</button>
            <div id="airesult"></div>
        </div>

        <script>
        async function convertCurrency() {
            const amount = parseFloat(document.getElementById("amount").value);
            const from_currency = document.getElementById("from_currency").value;
            const to_currency = document.getElementById("to_currency").value;
            document.getElementById("result").innerText = "Converting...";

            try {
                const response = await fetch("/api/convert", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ amount, from_currency, to_currency })
                });
                const data = await response.json();
                document.getElementById("result").innerText = data.result || data.error;
            } catch (e) {
                document.getElementById("result").innerText = "Error processing request";
            }
        }

        async function askAI() {
            const message = document.getElementById("question").value;
            document.getElementById("airesult").innerText = "AI is processing...";

            try {
                const response = await fetch("/api/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message })
                });
                const data = await response.json();
                document.getElementById("airesult").innerText = data.response || data.error;
            } catch (e) {
                document.getElementById("airesult").innerText = "Error processing request";
            }
        }
        </script>
    </body>
    </html>
    """

handler = Mangum(app)
