import streamlit as st
import requests

from agents import ask_currency_agent


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Currency Converter",
    page_icon="💱",
    layout="centered"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .result {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #444;
        margin-top: 20px;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="title">💱 AI Currency Converter</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Live currency conversion powered by AI'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# CURRENCY LIST
# --------------------------------------------------

currencies = [
    "USD",
    "EUR",
    "INR",
    "GBP",
    "JPY",
    "CAD",
    "AUD",
    "CHF",
    "CNY",
    "SGD"
]


# --------------------------------------------------
# MANUAL CURRENCY CONVERTER
# --------------------------------------------------

st.header("💰 Currency Converter")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input(
        "Amount",
        min_value=0.01,
        value=100.0,
        step=1.0
    )

    from_currency = st.selectbox(
        "From Currency",
        currencies,
        index=1
    )


with col2:

    to_currency = st.selectbox(
        "To Currency",
        currencies,
        index=2
    )


convert_button = st.button(
    "🔄 Convert",
    use_container_width=True
)


if convert_button:

    if from_currency == to_currency:

        st.success(
            f"{amount:.2f} {from_currency} = "
            f"{amount:.2f} {to_currency}"
        )

    else:

        url = (
            f"https://api.frankfurter.dev/v2/rate/"
            f"{from_currency}/{to_currency}"
        )

        try:

            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            rate = data["rate"]
            date = data["date"]

            converted_amount = amount * rate

            st.markdown(
                f"""
                <div class="result">

                <h2>
                {amount:.2f} {from_currency}
                =
                {converted_amount:.2f} {to_currency}
                </h2>

                <p>
                Exchange Rate:
                1 {from_currency} =
                {rate:.6f} {to_currency}
                </p>

                <p>
                Rate Date: {date}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Currency API Error: {e}"
            )


# --------------------------------------------------
# AI CURRENCY ASSISTANT
# --------------------------------------------------

st.divider()

st.header("🤖 Ask AI")

st.write(
    "You can also ask the AI to perform currency conversions "
    "using natural language."
)


user_input = st.chat_input(
    "Example: Convert 500 USD to INR"
)


if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        with st.spinner(
            "AI is getting the latest exchange rate..."
        ):

            try:

                response = ask_currency_agent(
                    user_input
                )

                st.write(response)

            except Exception as e:

                st.error(
                    f"AI Error: {e}"
                )


# --------------------------------------------------
# EXAMPLES
# --------------------------------------------------

st.divider()

st.subheader("💡 Example AI Questions")

st.markdown(
    """
    **Try these:**

    - Convert 100 EUR to INR
    - Convert 500 USD to INR
    - Convert 1000 INR to USD
    - Convert 250 GBP to EUR
    - Convert 100 CAD to INR
    """
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Built with Python • LangChain • Hugging Face • "
    "Frankfurter API • Streamlit"
)