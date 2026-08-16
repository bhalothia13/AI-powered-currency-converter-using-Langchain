import requests
from langchain_core.tools import tool


@tool
def currency_converter(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """
    Convert an amount from one currency to another
    using the latest available exchange rate.

    Args:
        amount: Amount to convert.
        from_currency: Source currency code, e.g. USD, EUR, INR.
        to_currency: Target currency code, e.g. USD, EUR, INR.

    Returns:
        Converted amount, exchange rate, and rate date.
    """

    # Convert currency codes to uppercase
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    # Validate amount
    if amount < 0:
        return "Amount cannot be negative."

    # Same currency
    if from_currency == to_currency:
        return (
            f"{amount:.2f} {from_currency} = "
            f"{amount:.2f} {to_currency}\n"
            f"Exchange rate: 1 {from_currency} = "
            f"1 {to_currency}"
        )

    # Frankfurter API
    url = (
        f"https://api.frankfurter.dev/v2/rate/"
        f"{from_currency}/{to_currency}"
    )

    try:
        # API request
        response = requests.get(
            url,
            timeout=10
        )

        # Check API response
        response.raise_for_status()

        # Convert response to JSON
        data = response.json()

        # Get exchange rate
        rate = data["rate"]

        # Get date
        date = data["date"]

        # Calculate converted amount
        converted_amount = amount * rate

        # Return result
        return (
            f"{amount:.2f} {from_currency} = "
            f"{converted_amount:.2f} {to_currency}\n"
            f"Exchange rate: 1 {from_currency} = "
            f"{rate:.6f} {to_currency}\n"
            f"Rate date: {date}"
        )

    except requests.exceptions.HTTPError:
        return (
            f"Unable to find exchange rate for "
            f"{from_currency} to {to_currency}."
        )

    except requests.exceptions.RequestException as e:
        return f"Currency API error: {str(e)}"

    except KeyError:
        return "Invalid response received from currency API."