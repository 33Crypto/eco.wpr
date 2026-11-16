# Private Market Monitor

A local Python command-line tool that displays public spot prices from Coinbase
Advanced Trade or YoBit. It does not place trades or need exchange credentials.

## Run

Requires Python 3.11 or newer.

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -e .
market-monitor
```

By default, the tool refreshes BTC-USD and ETH-USD prices every 30 seconds. Set
the products and refresh interval explicitly, or fetch one snapshot:

```sh
market-monitor --products BTC-USD SOL-USD --interval 15
market-monitor --products BTC-USD --once
```

For YoBit, choose the exchange and use lowercase pair names separated by an
underscore. It defaults to `btc_usd`:

```sh
market-monitor --exchange yobit --once
market-monitor --exchange yobit --products btc_usd eth_btc --interval 30
```

YoBit prices are the last trade reported by the exchange, which may be old for
an inactive market. The displayed update time is when the monitor fetched data,
not necessarily when the last trade occurred.

Prices are retrieved from Coinbase's public
[Get Public Product API](https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/public/get-public-product).
The monitor only reads market data; it does not provide investment advice.
