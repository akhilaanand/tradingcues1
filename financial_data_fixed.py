import yfinance as yf
import datetime
import json
import requests
from datetime import timedelta

API_KEY = "e5b94614ba607e9725122f6ce56e5e2e"
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_recent_fred_data(series_id, label):
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    observations = data.get("observations", [])
    if len(observations) < 2:
        return None
    
    latest_obs = observations[-1]
    latest_date = datetime.datetime.strptime(latest_obs["date"], "%Y-%m-%d").date()
    latest_value = latest_obs["value"]

    if datetime.datetime.now().date() - latest_date <= timedelta(days=1):
        return f"*{label} Update*: {latest_value} (as of {latest_date})"
    return None

def get_economic_updates():
    updates = []
    updates.append(fetch_recent_fred_data("FEDFUNDS", "Fed Rate"))
    updates.append(fetch_recent_fred_data("CPIAUCSL", "US CPI"))
    updates.append(fetch_recent_fred_data("UNRATE", "Unemployment Rate"))
    return [u for u in updates if u]

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

def fetch_fii_dii_data():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nseindia.com/',
    }
    session = requests.Session()

    try:
        session.get("https://www.nseindia.com", headers=headers)
        fii_dii_url = "https://www.nseindia.com/api/fii-dii?type=equity"
        response = session.get(fii_dii_url, headers=headers)
        if response.status_code != 200 or not response.content.strip():
            raise ValueError("Empty or bad response from NSE")
        data = response.json()
    except Exception as e:
        print(f"Error fetching FII/DII data: {e}")
        return "*FII/DII Activity*: Unable to fetch data ⚠️"

    last_entry = data['data'][-1]
    fii_buy = float(last_entry['fii_buy_value'])
    fii_sell = float(last_entry['fii_sell_value'])
    fii_net = fii_buy - fii_sell

    dii_buy = float(last_entry['dii_buy_value'])
    dii_sell = float(last_entry['dii_sell_value'])
    dii_net = dii_buy - dii_sell

    fii_sign = "🟢" if fii_net >= 0 else "🔴"
    dii_sign = "🟢" if dii_net >= 0 else "🔴"

    table = f"""
*FII/DII Activity (Yesterday)* 📊
| Investor | Buy (₹ Cr) | Sell (₹ Cr) | Net (₹ Cr) |
|----------|------------|-------------|------------|
| FII      | {fii_buy:.2f}     | {fii_sell:.2f}     | {fii_net:+.2f} {fii_sign}     |
| DII      | {dii_buy:.2f}     | {dii_sell:.2f}     | {dii_net:+.2f} {dii_sign}     |
"""
    return table

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

    updates = get_economic_updates()
    fii_dii_text = fetch_fii_dii_data()

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

    print("\n" + fii_dii_text)

    if updates:
        print("\n*Recent Economic Updates* 📈")
        for update in updates:
            print(update)

if __name__ == "__main__":
    try:
        build_summary()
    except Exception as e:
        print(f"Error in main function: {e}")
