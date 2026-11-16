import io
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from unittest.mock import patch

from market_monitor.cli import main
from market_monitor.coinbase import ProductPrice


class CLITests(unittest.TestCase):
    @patch("market_monitor.cli.get_spot_price")
    def test_once_prints_prices_and_exits(self, get_spot_price):
        get_spot_price.side_effect = [
            ProductPrice("BTC-USD", Decimal("67123.4500")),
            ProductPrice("ETH-USD", Decimal("2500")),
        ]
        output = io.StringIO()

        with redirect_stdout(output):
            result = main(["--once"])

        self.assertEqual(result, 0)
        self.assertIn("BTC-USD      67,123.45", output.getvalue())
        self.assertIn("ETH-USD      2,500", output.getvalue())
        self.assertEqual(get_spot_price.call_count, 2)

    @patch("market_monitor.cli.get_yobit_price")
    def test_selects_yobit_and_default_pair(self, get_yobit_price):
        get_yobit_price.return_value = ProductPrice("btc_usd", Decimal("67000"))
        output = io.StringIO()

        with redirect_stdout(output):
            result = main(["--exchange", "yobit", "--once"])

        self.assertEqual(result, 0)
        get_yobit_price.assert_called_once_with("btc_usd")
        self.assertIn("btc_usd      67,000", output.getvalue())


if __name__ == "__main__":
    unittest.main()
