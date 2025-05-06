import yfinance as yf
import datetime
import json
import requests
from datetime import timedelta

# FRED API setup
API_KEY = "e5b94614ba607e9725122f6ce56e5e2e"  # Replace with your FRED API key
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def fetch_recent_fred_data(series_id, label):
    """Fetches the latest data for a given FRED series ID and checks if released in the last 24 hours."""
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

    # Only include if released in the last 24 hours
    if datetime.datetime.today().date() - latest_date <= timedelta(days=1):
        return f"*{label} Update*: {latest_value} (as of {latest_date})"
    return None

def get_economic_updates():
    """Get recent economic data updates from FRED."""
    updates = []
    updates.append(fetch_recent_fred_data("FEDFUNDS", "Fed Rate"))
    updates.append(fetch_recent_fred_data("CPIAUCSL", "US CPI"))
    updates.append(fetch_recent_fred_data("UNRATE", "Unemployment Rate"))
    return [u for u in updates if u]

def fetch_data(symbol):
    """Fetches the latest data for the symbol."""
    print(f"Fetching data for {symbol}...")
    data = yf.download(symbol, period="2d")
    if data.empty or len(data) < 2:
        print(f"Warning: No data found for {symbol}")
        return None, None
    
    latest = float(data['Close'].iloc[-1])
    previous = float(data['Close'].iloc[-2])
    
    return latest, previous

def build_summary():
    """Builds the market summary including VIX, S&P500, Crude Oil, Gold, USD/INR, and economic updates."""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"Trade setup for {today}")
    print("-" * 50)
    
    # VIX
    vix_latest, vix_previous = fetch_data('^VIX')
    if vix_latest is None:
        vix_change = vix_percent_change = vix_direction = "N/A"
    else:
        vix_change = vix_latest - vix_previous
        vix_percent_change = (vix_change / vix_previous) * 100
        vix_direction = "UP 🟢" if vix_change >= 0 else "DOWN 🔴"

    # S&P 500
    sp500_latest, sp500_previous = fetch_data('^GSPC')
    if sp500_latest is None:
        sp500_direction = "N/A"
    else:
        sp500_direction = "bullish 🟢" if sp500_latest > sp500_previous else "bearish 🔴"
    
    # Crude Oil
    crude_latest, crude_previous = fetch_data('CL=F')
    if crude_latest is None:
        crude_change = crude_percent_change = crude_direction = "N/A"
    else:
        crude_change = crude_latest - crude_previous
        crude_percent_change = (crude_change / crude_previous) * 100
        crude_direction = "UP 🟢" if crude_change >= 0 else "DOWN 🔴"
    
    # Gold
    gold_latest, gold_previous = fetch_data('GC=F')
    if gold_latest is None:
        gold_change = gold_percent_change = gold_direction = "N/A"
    else:
        gold_change = gold_latest - gold_previous
        gold_percent_change = (gold_change / gold_previous) * 100
        gold_direction = "UP 🟢" if gold_change >= 0 else "DOWN 🔴"
    
    # USD/INR
    usd_inr_latest, usd_inr_previous = fetch_data('INR=X')
    if usd_inr_latest is None:
        usd_inr_change = usd_inr_percent_change = "N/A"
    else:
        usd_inr_change = usd_inr_latest - usd_inr_previous
        usd_inr_percent_change = (usd_inr_change / usd_inr_previous) * 100
    
    # Hang Seng
    hang_seng_latest, hang_seng_previous = fetch_data('^HSI')
    if hang_seng_latest is None:
        hang_seng_direction = "N/A"
    else:
        hang_seng_direction = "bullish 🟢" if hang_seng_latest > hang_seng_previous else "bearish 🔴"
    
    # Economic updates
    economic_updates = get_economic_updates()
    
    # Build summary text
    summary_text = f"*Trade setup for {today}*\n"
    summary_text += "-" * 50 + "\n\n"

    summary_text += f"*VIX*: {vix_latest} {vix_direction} +{vix_change:.2f} ({vix_percent_change:.2f}%)\n"
    summary_text += f"S&P 500: {sp500_latest} {sp500_direction}\n"
    summary_text += f"*Crude Oil*: {crude_latest} {crude_direction} +{crude_change:.2f} ({crude_percent_change:.2f}%)\n"
    summary_text += f"*Gold*: {gold_latest} {gold_direction} +{gold_change:.2f} ({gold_percent_change:.2f}%)\n"
    summary_text += f"*USD/INR*: {usd_inr_latest} {usd_inr_change:.2f} (+{usd_inr_percent_change:.2f}%)\n"
    summary_text += f"Hang Seng: {hang_seng_latest} {hang_seng_direction}\n"
    
    if economic_updates:
        summary_text += "\n*US Economic Updates*\n"
        for update in economic_updates:
            summary_text += f"{update}\n"

    return summary_text

def save_to_files(summary_text):
    """Saves the summary text to files."""
    with open('market_summary.txt', 'w') as f:
        f.write(summary_text)
    
    print("Summary written to market_summary.txt")

def main():
    try:
        summary_text = build_summary()
        save_to_files(summary_text)
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
