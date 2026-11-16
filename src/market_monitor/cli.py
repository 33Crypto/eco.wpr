import argparse
import math
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal

from market_monitor.coinbase import CoinbaseAPIError, get_spot_price


def _format_price(price: Decimal) -> str:
    formatted = format(price, ",f")
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Monitor public spot prices from Coinbase Advanced Trade."
    )
    parser.add_argument(
        "--products",
        nargs="+",
        default=["BTC-USD", "ETH-USD"],
        metavar="PRODUCT",
        help="Coinbase product IDs to monitor (default: BTC-USD ETH-USD)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=30.0,
        help="Seconds between updates (default: 30)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Fetch one snapshot and exit",
    )
    args = parser.parse_args(argv)
    if not math.isfinite(args.interval) or args.interval <= 0:
        parser.error("--interval must be a finite number greater than zero")

    try:
        while True:
            updated = datetime.now(timezone.utc).isoformat(timespec="seconds")
            print(f"Updated {updated}")
            for product_id in args.products:
                product = get_spot_price(product_id)
                print(f"{product.product_id:12} {_format_price(product.price)}")
            if args.once:
                return 0
            print()
            time.sleep(args.interval)
    except (CoinbaseAPIError, ValueError) as exc:
        print(f"market-monitor: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
