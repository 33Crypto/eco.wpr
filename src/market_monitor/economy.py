import csv
import io
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class EconomicDataError(Exception):
    """Raised when an economic data series cannot be retrieved or interpreted."""


def fetch_series(series_id: str) -> dict[date, Decimal]:
    request = Request(
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}",
        headers={"Accept": "text/csv"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            text = response.read().decode("utf-8-sig")
    except HTTPError as exc:
        raise EconomicDataError(f"FRED returned HTTP {exc.code} for {series_id}") from exc
    except URLError as exc:
        raise EconomicDataError(f"Could not reach FRED: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise EconomicDataError(f"Could not reach FRED: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise EconomicDataError(f"FRED returned invalid text for {series_id}") from exc

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "observation_date" not in reader.fieldnames or series_id not in reader.fieldnames:
        raise EconomicDataError(f"FRED returned unexpected CSV for {series_id}")

    observations = {}
    try:
        for row in reader:
            value = row[series_id]
            if value in ("", "."):
                continue
            observed = date.fromisoformat(row["observation_date"])
            number = Decimal(value)
            if not number.is_finite() or number < 0:
                raise ValueError("invalid value")
            observations[observed] = number
    except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
        raise EconomicDataError(f"FRED returned invalid data for {series_id}") from exc
    if not observations:
        raise EconomicDataError(f"FRED returned no observations for {series_id}")
    return observations


def _previous_month(observed: date, months: int) -> date:
    absolute_month = observed.year * 12 + observed.month - 1 - months
    return date(absolute_month // 12, absolute_month % 12 + 1, 1)


def _latest(series_id: str) -> tuple[date, Decimal, dict[date, Decimal]]:
    observations = fetch_series(series_id)
    observed = max(observations)
    return observed, observations[observed], observations


def _change(
    series_id: str, months: int, annualize: bool = False
) -> tuple[date, Decimal]:
    observed, value, observations = _latest(series_id)
    previous_date = _previous_month(observed, months)
    previous = observations.get(previous_date)
    if previous is None or previous <= 0:
        raise EconomicDataError(
            f"FRED has no usable {series_id} observation for {previous_date}"
        )
    ratio = value / previous
    if annualize:
        ratio = ratio ** 4
    return observed, (ratio - 1) * 100


def main() -> int:
    try:
        inflation_date, inflation = _change("CPIAUCNS", 12)
        unemployment_date, unemployment, _ = _latest("UNRATE")
        gdp_date, gdp = _change("GDPC1", 3, annualize=True)
        spending_date, spending = _change("PCEC96", 1)
    except EconomicDataError as exc:
        print(f"economy-monitor: {exc}", file=sys.stderr)
        return 1

    print("U.S. economic snapshot (source: FRED; data from BLS and BEA)")
    print(f"Inflation, CPI year-over-year: {inflation:.2f}% ({inflation_date:%Y-%m})")
    print(f"Unemployment rate: {unemployment:.2f}% ({unemployment_date:%Y-%m})")
    print(f"Real GDP growth, quarterly annualized: {gdp:.2f}% (quarter starting {gdp_date})")
    print(f"Real consumer spending, month-over-month: {spending:.2f}% ({spending_date:%Y-%m})")
    print("Observation periods differ; figures may be revised.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
