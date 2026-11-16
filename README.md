# Private Market Monitor

A local Python command-line tool that displays public spot prices from Coinbase
Advanced Trade. It does not place trades and does not need Coinbase credentials.

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

Prices are retrieved from Coinbase's public
[Get Public Product API](https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/public/get-public-product).
The monitor only reads market data; it does not provide investment advice.
