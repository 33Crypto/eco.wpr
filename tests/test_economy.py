import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date
from decimal import Decimal
from unittest.mock import patch
from urllib.error import URLError

from market_monitor.economy import EconomicDataError, fetch_series, main


class EconomyTests(unittest.TestCase):
    @patch("market_monitor.economy.urlopen")
    def test_reads_csv_and_skips_missing_observations(self, urlopen):
        urlopen.return_value = io.BytesIO(
            b"observation_date,UNRATE\n2025-01-01,4.0\n2025-02-01,\n"
        )
        self.assertEqual(fetch_series("UNRATE"), {date(2025, 1, 1): Decimal("4.0")})
        self.assertEqual(
            urlopen.call_args.args[0].full_url,
            "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE",
        )

    @patch("market_monitor.economy.urlopen")
    def test_rejects_unexpected_csv(self, urlopen):
        urlopen.return_value = io.BytesIO(b"error,message\nrate limit,try later\n")
        with self.assertRaisesRegex(EconomicDataError, "unexpected CSV"):
            fetch_series("UNRATE")

    @patch("market_monitor.economy.urlopen")
    def test_reports_network_failure(self, urlopen):
        urlopen.side_effect = URLError("unavailable")
        with self.assertRaisesRegex(EconomicDataError, "unavailable"):
            fetch_series("UNRATE")

    @patch("market_monitor.economy.fetch_series")
    def test_snapshot_calculates_indicators_from_correct_periods(self, fetch):
        fetch.side_effect = {
            "CPIAUCNS": {
                date(2024, 12, 1): Decimal("100"),
                date(2025, 12, 1): Decimal("103"),
            },
            "UNRATE": {date(2025, 11, 1): Decimal("4.2")},
            "GDPC1": {
                date(2025, 7, 1): Decimal("100"),
                date(2025, 10, 1): Decimal("101"),
            },
            "PCEC96": {
                date(2025, 11, 1): Decimal("100"),
                date(2025, 12, 1): Decimal("100.5"),
            },
        }.__getitem__
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(), 0)
        self.assertIn("CPI year-over-year: 3.00% (2025-12)", output.getvalue())
        self.assertIn("Unemployment rate: 4.20% (2025-11)", output.getvalue())
        self.assertIn("quarterly annualized: 4.06%", output.getvalue())
        self.assertIn("month-over-month: 0.50% (2025-12)", output.getvalue())

    @patch("market_monitor.economy.fetch_series")
    def test_missing_comparison_period_fails_instead_of_guessing(self, fetch):
        fetch.return_value = {
            date(2025, 12, 1): Decimal("103"),
            date(2024, 11, 1): Decimal("100"),
        }
        error = io.StringIO()
        with redirect_stderr(error):
            self.assertEqual(main(), 1)
        self.assertIn("no usable CPIAUCNS observation for 2024-12-01", error.getvalue())
