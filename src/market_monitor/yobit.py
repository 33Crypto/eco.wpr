import json
import re
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from market_monitor.coinbase import ProductPrice


_BASE_URL = "https://yobit.net/api/3/ticker"
_PRODUCT_ID = re.compile(r"[a-z0-9]+_[a-z0-9]+")


class YoBitAPIError(Exception):
    """Raised when YoBit returns an unusable market-data response."""


def get_spot_price(product_id: str, timeout: float = 10.0) -> ProductPrice:
    if not _PRODUCT_ID.fullmatch(product_id):
        raise ValueError(f"Invalid YoBit pair: {product_id!r} (example: btc_usd)")

    request = Request(f"{_BASE_URL}/{product_id}", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response, parse_float=Decimal)
    except HTTPError as exc:
        raise YoBitAPIError(f"YoBit returned HTTP {exc.code} for {product_id}") from exc
    except URLError as exc:
        raise YoBitAPIError(f"Could not reach YoBit: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise YoBitAPIError(f"Could not reach YoBit: {exc}") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise YoBitAPIError("YoBit returned invalid JSON") from exc

    if isinstance(payload, dict) and "error" in payload:
        raise YoBitAPIError(f"YoBit error for {product_id}: {payload['error']}")
    ticker = payload.get(product_id) if isinstance(payload, dict) else None
    if not isinstance(ticker, dict):
        raise YoBitAPIError(f"YoBit returned no ticker for {product_id}")

    try:
        price = Decimal(ticker["last"])
    except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
        raise YoBitAPIError(f"YoBit returned an invalid price for {product_id}") from exc
    if not price.is_finite() or price < 0:
        raise YoBitAPIError(f"YoBit returned an invalid price for {product_id}")

    return ProductPrice(product_id=product_id, price=price)
