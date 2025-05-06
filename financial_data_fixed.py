import yfinance as yf
import datetime
import os

def fetch_latest_data(ticker, label):
    print(f"Fetching data for {label} ({ticker})...")
    data = yf.download(ticker, period="7d", interval="1d", progress=False)
    data = data.dropna()
    if not data.empty and len(data) >= 2:
        latest = float(data['Close'].iloc[-1])
        previous = float(data['Close'].iloc[-2])
        change = latest - previous
        percent_change = (change / previous) * 100 if previous != 0 else 0
        return latest, change, percent_change
    else:
        print(f"Warning: No data found or insufficient data for {label}")
        return None, None, None

def format_change(change, percent_change):
    if change >= 0:
        return f"🟢 +{change:.2f} (+{percent_change:.2f}%)", "🟢", "UP"
    else:
        return f"🔴 {change:.2f} ({percent_change:.2f}%)", "🔴", "DOWN"

def main():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"Trade setup for {today}")
    print("-" * 50)
    summary_lines = [f"*Trade setup for {today}*", "-" * 50]

    assets = [
        {'ticker': '^VIX', 'label': 'VIX'},
        {'ticker': '^GSPC', 'label': 'S&P 500'},
        {'ticker': 'GC=F', 'label': 'Gold'},
        {'ticker': 'CL=F', 'label': 'Crude Oil'},
        {'ticker': 'DX-Y.NYB', 'label': 'USD Index'},
        {'ticker': 'USDINR=X', 'label': 'INR'},
        {'ticker': '^HSI', 'label': 'Hang Seng'},
    ]

    for asset in assets:
        latest, change, pct = fetch_latest_data(asset['ticker'], asset['label'])
        if latest is None:
            continue

        emoji_line, dot, direction = format_change(change, pct)

        if asset['label'] == 'VIX':
            summary_lines.append(f"*VIX*: {latest:.2f} {emoji_line}")
            summary_lines.append(f"Market Volatility is *{direction} {dot}*")
            summary_lines.append("")
        elif asset['label'] == 'S&P 500':
            summary_lines.append(f"*S&P 500*: {latest:.2f} {dot}")
            summary_lines.append(f"S&P 500 looks *{'bullish' if change >= 0 else 'bearish'} {dot}*")
            summary_lines.append("")
        elif asset['label'] == 'Gold':
            summary_lines.append(f"*Gold*: {latest:.2f}")
            summary_lines.append(f"{emoji_line}")
            summary_lines.append("")
        elif asset['label'] == 'Crude Oil':
            summary_lines.append(f"*Crude Oil*: {latest:.2f}")
            summary_lines.append(f"{emoji_line}")
            summary_lines.append("")
        elif asset['label'] == 'USD Index':
            summary_lines.append(f"*USD Index*: {latest:.2f}")
            summary_lines.append(f"{emoji_line}")
            summary_lines.append("")
        elif asset['label'] == 'INR':
            summary_lines.append(f"*INR (₹ per USD)*: {latest:.2f}")
            summary_lines.append(f"{emoji_line}")
            summary_lines.append("")
        elif asset['label'] == 'Hang Seng':
            summary_lines.append(f"*Hang Seng*: {latest:.2f} {dot}")
            summary_lines.append(f"Hang Seng looks *{'bullish' if change >= 0 else 'bearish'} {dot}*")
            summary_lines.append("")

    output_text = "\n".join(summary_lines)
    with open('market_summary.txt', 'w') as f:
        f.write(output_text)
    print("\nSummary written to market_summary.txt")

if __name__ == "__main__":
    main()
