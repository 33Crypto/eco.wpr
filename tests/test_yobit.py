import io
import unittest
from decimal import Decimal
from unittest.mock import patch
from urllib.error import URLError

from market_monitor.yobit import YoBitAPIError, get_spot_price


class YoBitTests(unittest.TestCase):
    @patch("market_monitor.yobit.urlopen")
    def test_fetches_last_trade_without_losing_precision(self, urlopen):
        urlopen.return_value = io.BytesIO(b'{"btc_usd":{"last":67123.12345678}}')

        product = get_spot_price("btc_usd")

        self.assertEqual(product.price, Decimal("67123.12345678"))
        self.assertEqual(
            urlopen.call_args.args[0].full_url,
            "https://yobit.net/api/3/ticker/btc_usd",
        )

    def test_rejects_invalid_pair_without_network_request(self):
        with patch("market_monitor.yobit.urlopen") as urlopen:
            with self.assertRaises(ValueError):
                get_spot_price("../btc_usd")
        urlopen.assert_not_called()

    @patch("market_monitor.yobit.urlopen")
    def test_reports_api_error(self, urlopen):
        urlopen.return_value = io.BytesIO(b'{"error":"invalid pair"}')
        with self.assertRaisesRegex(YoBitAPIError, "invalid pair"):
            get_spot_price("btc_usd")

    @patch("market_monitor.yobit.urlopen")
    def test_reports_network_failure(self, urlopen):
        urlopen.side_effect = URLError("unavailable")
        with self.assertRaisesRegex(YoBitAPIError, "unavailable"):
            get_spot_price("btc_usd")

    @patch("market_monitor.yobit.urlopen")
    def test_rejects_missing_price(self, urlopen):
        urlopen.return_value = io.BytesIO(b'{"btc_usd":{}}')
        with self.assertRaisesRegex(YoBitAPIError, "invalid price"):
            get_spot_price("btc_usd")
