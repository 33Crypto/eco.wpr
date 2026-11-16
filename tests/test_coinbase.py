import io
import json
import unittest
from decimal import Decimal
from unittest.mock import patch

from market_monitor.coinbase import CoinbaseAPIError, get_spot_price


class CoinbaseTests(unittest.TestCase):
    @patch("market_monitor.coinbase.urlopen")
    def test_fetches_public_product_price(self, urlopen):
        response = io.BytesIO(
            json.dumps({"product_id": "BTC-USD", "price": "67123.45"}).encode()
        )
        response.__enter__ = lambda: response
        response.__exit__ = lambda *_: None
        urlopen.return_value = response

        product = get_spot_price("BTC-USD")

        self.assertEqual(product.product_id, "BTC-USD")
        self.assertEqual(product.price, Decimal("67123.45"))
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://api.coinbase.com/api/v3/brokerage/market/products/BTC-USD",
        )

    def test_rejects_malformed_product_id_without_network_request(self):
        with patch("market_monitor.coinbase.urlopen") as urlopen:
            with self.assertRaises(ValueError):
                get_spot_price("../BTC-USD")
        urlopen.assert_not_called()

    @patch("market_monitor.coinbase.urlopen")
    def test_rejects_unexpected_product_response(self, urlopen):
        response = io.BytesIO(
            json.dumps({"product_id": "ETH-USD", "price": "2500"}).encode()
        )
        response.__enter__ = lambda: response
        response.__exit__ = lambda *_: None
        urlopen.return_value = response

        with self.assertRaises(CoinbaseAPIError):
            get_spot_price("BTC-USD")


if __name__ == "__main__":
    unittest.main()
