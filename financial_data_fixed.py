import yfinance as yf
import datetime
import requests
from datetime import timedelta
from contextlib import redirect_stdout

API_KEY = "e5b94614ba607e9725122f6ce56e5e2e"
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_recent_fred_data(series_id, label, formatter=None):
    try:
        data = fred.get_series(series_id)
        if data.empty:
            return None

        last_date = data.index[-1].to_pydatetime().date()
        today = datetime.now().date()

        # ✅ 24-hour freshness check
        if today - last_date > timedelta(days=1):
            return None

        latest = data.iloc[-1]
        previous = data.iloc[-2] if len(data) > 1 else None

        # Optional: use a formatter like format_cpi if passed
        if formatter:
            return formatter(label, latest, previous, last_date)

        # Default simple format with direction
        change = latest - previous if previous is not None else 0
        direction = "🔻" if change < 0 else "🟢" if change > 0 else "➡️"
        change_str = f"{change:.2f}" if previous is not None else "—"
        return f"*{label}*: {latest:.2f} ({direction}, {change_str}) — as of {last_date}"

    except Exception as e:
        print(f"Error fetching {label}: {e}")
        return None

def get_us_macro_updates():
    updates = [
        fetch_recent_fred_data("FEDFUNDS", "Fed Funds Rate"),
        fetch_recent_fred_data("CPIAUCSL", "US CPI", format_cpi),
        fetch_recent_fred_data("GDP", "US GDP", format_gdp),
        fetch_recent_fred_data("UNRATE", "Unemployment Rate")
    ]
    updates = [u for u in updates if u]
    if not updates:
        return ["There is no new US macro update for the updates you follow."]
    return updates

def fetch_data(symbol):
    print(f"Fetching data for {symbol}...")
    data = yf.download(symbol, period="7d", progress=False)
    if data.empty or len(data['Close'].dropna()) < 2:
        print(f"Warning: No data found for {symbol}")
        return None, None

    clean_close = data['Close'].dropna()
    latest = clean_close.iloc[-1].item()
    previous = clean_close.iloc[-2].item()
    return latest, previous

def build_summary():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"Trade setup for {today}")
    print("-" * 50)

    vix_latest, vix_previous = fetch_data('^VIX')
    sp500_latest, sp500_previous = fetch_data('^GSPC')
    crude_latest, crude_previous = fetch_data('CL=F')
    gold_latest, gold_previous = fetch_data('GC=F')
    inr_latest, inr_previous = fetch_data('INR=X')
    hsi_latest, hsi_previous = fetch_data('^HSI')

    macro_updates = get_us_macro_updates()

    def format_change(latest, previous):
        if latest is None or previous is None:
            return "N/A", "N/A", "N/A"
        change = latest - previous
        percent = (change / previous) * 100
        direction = "🟢 UP" if change >= 0 else "🔴 DOWN"
        return f"{latest:.2f}", f"{percent:.2f}%", direction

    vix_val, vix_pct, vix_dir = format_change(vix_latest, vix_previous)
    crude_val, crude_pct, crude_dir = format_change(crude_latest, crude_previous)
    gold_val, gold_pct, gold_dir = format_change(gold_latest, gold_previous)

    print(f"\n*VIX*: {vix_val} ({vix_dir}, {vix_pct})")
    print(f"*S&P 500*: {sp500_latest:.2f}" if sp500_latest else "*S&P 500*: N/A")
    print(f"*Crude*: {crude_val} ({crude_dir}, {crude_pct})")
    print(f"*Gold*: {gold_val} ({gold_dir}, {gold_pct})")
    print(f"*USD/INR*: {inr_latest:.2f}" if inr_latest else "*USD/INR*: N/A")
    print(f"*Hang Seng*: {hsi_latest:.2f}" if hsi_latest else "*Hang Seng*: N/A")

    print("\nUS Macro Updates 🏛️")
    for line in macro_updates:
        print(line)

with open("market_summary.txt", "w", encoding="utf-8") as f:
    with redirect_stdout(f):
        build_summary()

# Also print to terminal
build_summary()
