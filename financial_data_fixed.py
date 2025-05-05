import yfinance as yf
import datetime
import json
import os

def fetch_data(ticker, label):
    try:
        print(f"Fetching data for {label} ({ticker})...")
        data = yf.download(ticker, period="2d", progress=False)

        if data.empty or len(data) < 2:
            print(f"Warning: No data found for {label}")
            return None

        print(f"Raw data for {label}:")
        print(data.tail(2))

        latest = float(data['Close'].iloc[-1])
        previous = float(data['Close'].iloc[-2])
        change = latest - previous
        percent_change = (change / previous) * 100
        direction_arrow = "↑" if change >= 0 else "↓"
        sentiment_dot = "🟢" if change >= 0 else "🔴"
        sentiment_word = "bullish" if change >= 0 else "bearish"

        return {
            "label": label,
            "latest": latest,
            "change": change,
            "percent_change": percent_change,
            "arrow": direction_arrow,
            "dot": sentiment_dot,
            "sentiment": sentiment_word
        }

    except Exception as e:
        print(f"Error fetching data for {label}: {e}")
        return None

def main():
    try:
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print(f"Trade Setup for {today}")
        print("-" * 50)

        # Fetch individual data points
        vix = fetch_data('^VIX', 'VIX')
        sp500 = fetch_data('^GSPC', 'S&P 500')
        gold = fetch_data('GC=F', 'Gold')
        crude = fetch_data('CL=F', 'Crude Oil')

        summary = f"*Trade setup for {today}*\n"
        summary += "--------------------------------------------------\n"

        if vix:
            summary += f"*{vix['label']}*: {vix['latest']:.2f} {vix['arrow']} +{vix['change']:.2f} ({vix['percent_change']:.2f}%)\n"
            summary += f"Market Volatility is *UP {vix['dot']}*\n\n"

        if sp500:
            summary += f"*{sp500['label']}*: {sp500['latest']:.2f} {sp500['dot']}\n"
            summary += f"{sp500['label']} looks *{sp500['sentiment']} {sp500['dot']}*\n\n"

        if gold:
            summary += f"*{gold['label']}*: {gold['latest']:.2f} {gold['dot']}\n"
            summary += f"{'Up' if gold['change'] >= 0 else 'Down'} by {abs(gold['change']):.2f} ({abs(gold['percent_change']):.2f}%)\n\n"

        if crude:
            summary += f"*{crude['label']}*: {crude['latest']:.2f} {crude['dot']}\n"
            summary += f"{'Up' if crude['change'] >= 0 else 'Down'} by {abs(crude['change']):.2f} ({abs(crude['percent_change']):.2f}%)\n\n"

        # Save text file
        with open('market_summary.txt', 'w') as f:
            f.write(summary)

        print("\nSummary written to market_summary.txt")
        print(summary)

        # Optional: JSON output for structured use
        json_output = {
            "date": today,
            "vix": vix,
            "sp500": sp500,
            "gold": gold,
            "crude": crude
        }

        with open('market_summary.json', 'w') as jf:
            json.dump(json_output, jf, indent=2)

        print("JSON summary written to market_summary.json")

    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
