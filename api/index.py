import os
import sys

# Root directory ko Python path me add karna
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from mangum import Mangum

try:
    from tools import currency_converter
    from agents import ask_currency_agent
except Exception as e:
    print(f"Import Error: {e}")

app = FastAPI(title="AI Currency Converter")


# ==========================================
# 1. FRONTEND WEB UI ROUTE
# ==========================================
@app.get("/", response_class=HTMLResponse)
@app.get("/api/index", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
def frontend():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Currency Converter</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #f9f9f9; color: #333; }
            h1 { text-align: center; }
            .box { background: white; border: 1px solid #ddd; padding: 20px; margin-top: 20px; border-radius: 10px; }
            input, select, button { width: 100%; padding: 12px; margin: 8px 0; box-sizing: border-box; border: 1px solid #ccc; border-radius: 6px; font-size: 15px; }
            button { cursor: pointer; background-color: #0070f3; color: white; border: none; font-weight: bold; }
            #result, #airesult { margin-top: 15px; padding: 12px; background: #f0f4f8; border-radius: 6px; font-weight: bold; word-break: break-word; }
        </style>
    </head>
    <body>
        <h1>💱 AI Currency Converter</h1>

        <div class="box">
            <h2>Currency Converter</h2>
            <input id="amount" type="number" value="100" min="0.01" placeholder="Amount">
            <select id="from_currency">
                <option value="USD">USD</option><option value="EUR">EUR</option><option value="INR" selected>INR</option>
                <option value="GBP">GBP</option><option value="JPY">JPY</option><option value="CAD">CAD</option>
                <option value="AUD">AUD</option><option value="CHF">CHF</option><option value="CNY">CNY</option><option value="SGD">SGD</option>
            </select>
            <select id="to_currency">
                <option value="INR">INR</option><option value="USD" selected>USD</option><option value="EUR">EUR</option>
                <option value="GBP">GBP</option><option value="JPY">JPY</option><option value="CAD">CAD</option>
                <option value="AUD">AUD</option><option value="CHF">CHF</option><option value="CNY">CNY</option><option value="SGD">SGD</option>
            </select>
            <button onclick="convertCurrency()">🔄 Convert</button>
            <div id="result">Result will appear here...</div>
        </div>

        <div class="box">
            <h2>🤖 Ask AI</h2>
            <input id="question" placeholder="Example: Convert 500 USD to INR">
            <button onclick="askAI()">Ask AI</button>
            <div id="airesult">AI response will appear here...</div>
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
                document.getElementById("result").innerText = data.result || data.error || data.detail || JSON.stringify(data);
            } catch (e) {
                document.getElementById("result").innerText = "Error processing request";
            }
        }

        async function askAI() {
            const message = document.getElementById("question").value;
            if(!message) return alert("Please enter a question");
            document.getElementById("airesult").innerText = "AI is thinking...";

            try {
                const response = await fetch("/api/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message })
                });
                const data = await response.json();
                document.getElementById("airesult").innerText = data.response || data.error || data.detail || JSON.stringify(data);
            } catch (e) {
                document.getElementById("airesult").innerText = "Error processing request";
            }
        }
        </script>
    </body>
    </html>
    """


# ==========================================
# 2. ALL-IN-ONE POST HANDLER FOR VERCEL
# ==========================================
@app.post("/")
@app.post("/api/index")
@app.post("/api/convert")
@app.post("/convert")
@app.post("/api/ask")
@app.post("/ask")
async def handle_all_post_requests(request: Request):
    try:
        data = await request.json()

        # Check if it's a Currency Conversion Request
        if "amount" in data and "from_currency" in data and "to_currency" in data:
            result = currency_converter.invoke({
                "amount": float(data["amount"]),
                "from_currency": str(data["from_currency"]),
                "to_currency": str(data["to_currency"])
            })
            return {"result": result}

        # Check if it's an AI Agent Request
        elif "message" in data:
            result = ask_currency_agent(data["message"])
            return {"response": result}

        else:
            return {"error": "Invalid request payload"}

    except Exception as e:
        return {"error": str(e)}


handler = Mangum(app)
