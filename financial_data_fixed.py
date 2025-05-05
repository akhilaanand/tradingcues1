import yfinance as yf
import datetime
import json

def get_latest_two_valid_closes(ticker_name, label):
    print(f"Fetching data for {label} ({ticker_name})...")
    data = yf.download(ticker_name, period="7d", progress=False)

    if data.empty or len(data) < 2:
        print(f"Warning: Insufficient data for {label}")
        return None

    # Sort data by index (just in case) and take last two rows
    data = data.sort_index()
    latest = float(data['Close'].iloc[-1])
    previous = float(data['Close'].iloc[-2])
    change = latest - previous
    percent_change = (change / previous) * 100 if previous != 0 else 0
    direction = "UP 🟢" if change > 0 else "DOWN 🔴"

    return {
        "label": label,
        "latest": latest,
        "previous": previous,
        "change": change,
        "percent_change": percent_change,
        "direction": direction
    }

def format_section(title, data):
    arrow = "🟢" if data["change"] > 0 else "🔴"
    return f"*{title}*: {data['latest']:.2f} {arrow}\n{title} {'rose' if data['change'] > 0 else 'fell'} by {abs(data['change']):.2f} ({abs(data['percent_change']):.2f}%)\n"

def main():
    try:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print(f"Trade setup for {today}")
        print("-" * 50)

        summary = f"*Trade setup for {today}*\n" + "-"*50 + "\n"

        # VIX
        vix = get_latest_two_valid_closes("^VIX", "VIX")
        if vix:
            summary += f"*VIX*: {vix['latest']:.2f} ↑ +{vix['change']:.2f} ({vix['percent_change']:.2f}%)\n"
            summary += f"Market Volatility is *{vix['direction']}*\n\n"

        # S&P 500
        sp500 = get_latest_two_valid_closes("^GSPC", "S&P 500")
        if sp500:
            summary += f"*S&P 500*: {sp500['latest']:.2f} {'🟢' if sp500['change'] > 0 else '🔴'}\n"
            summary += f"S&P 500 looks *{'bullish 🟢' if sp500['change'] > 0 else 'bearish 🔴'}*\n\n"

        # Crude Oil
        crude = get_latest_two_valid_closes("CL=F", "Crude Oil")
        if crude:
            summary += format_section("Crude Oil", crude) + "\n"

        # Gold
        gold = get_latest_two_valid_closes("GC=F", "Gold")
        if gold:
            summary += format_section("Gold", gold) + "\n"

        print(summary)

        with open('market_summary.txt', 'w') as f:
            f.write(summary)

        print("Market summary written to market_summary.txt")

        # Optional: save as JSON
        all_data = {
            "date": today,
            "VIX": vix,
            "S&P 500": sp500,
            "Crude Oil": crude,
            "Gold": gold
        }

        with open('market_summary.json', 'w') as jf:
            json.dump(all_data, jf, indent=2)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
