import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


_BASE_URL = "https://api.coinbase.com/api/v3/brokerage/market/products"
_PRODUCT_ID = re.compile(r"[A-Z0-9]+-[A-Z0-9]+")


class CoinbaseAPIError(Exception):
    """Raised when Coinbase returns an unusable market-data response."""


@dataclass(frozen=True)
class ProductPrice:
    product_id: str
    price: Decimal


def get_spot_price(product_id: str, timeout: float = 10.0) -> ProductPrice:
    if not _PRODUCT_ID.fullmatch(product_id):
        raise ValueError(f"Invalid Coinbase product ID: {product_id!r}")

    request = Request(
        f"{_BASE_URL}/{product_id}",
        headers={"Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise CoinbaseAPIError(
            f"Coinbase returned HTTP {exc.code} for {product_id}"
        ) from exc
    except URLError as exc:
        raise CoinbaseAPIError(f"Could not reach Coinbase: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise CoinbaseAPIError("Coinbase returned invalid JSON") from exc

    if not isinstance(payload, dict) or payload.get("product_id") != product_id:
        raise CoinbaseAPIError(f"Coinbase returned an unexpected product for {product_id}")

    try:
        price = Decimal(payload["price"])
    except (KeyError, InvalidOperation, TypeError) as exc:
        raise CoinbaseAPIError(f"Coinbase returned an invalid price for {product_id}") from exc

    if not price.is_finite():
        raise CoinbaseAPIError(f"Coinbase returned a non-finite price for {product_id}")

    return ProductPrice(product_id=product_id, price=price)
