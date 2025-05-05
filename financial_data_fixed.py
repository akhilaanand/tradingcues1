import yfinance as yf
import datetime
import json

def main():
    try:
        # Get today's date
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print(f"Trade Setup for {today}")
        print("-" * 50)
        
        # Get VIX data
        print("Fetching VIX data...")
        data = yf.download('^VIX', period="2d")
        
        if data.empty or len(data) < 2:
            print("Warning: Insufficient VIX data")
            return
        
        print("\nRaw data:")
        print(data.tail(2))
        
        latest_close = float(data['Close'].iloc[-1])
        previous_close = float(data['Close'].iloc[-2])
        
        change = latest_close - previous_close
        percent_change = (change / previous_close) * 100
        is_up = change >= 0
        
        # Set direction emojis and colors
        if is_up:
            direction_text = "🟢⬆️ UP"
            arrow = "🟢⬆️"
        else:
            direction_text = "🔴🔻 DOWN"
            arrow = "🔴🔻"
        
        # Build Slack-formatted summary
        summary_text = f"*Trade Setup for {today}*\n"
        summary_text += "--------------------------------------------------\n"
        summary_text += f"*VIX*: {latest_close:.2f} {arrow} "
        summary_text += f"{change:+.2f} ({percent_change:+.2f}%)\n"
        summary_text += f"Market Volatility is *{direction_text}*\n"
        
        print("\nFormatted Slack message:\n")
        print(summary_text)
        
        # Write to text file
        with open('market_summary.txt', 'w') as f:
            f.write(summary_text)
        
        # Write JSON summary
        summary_json = {
            "date": today,
            "VIX": {
                "latest_close": latest_close,
                "previous_close": previous_close,
                "change": round(change, 2),
                "percent_change": round(percent_change, 2),
                "direction": "UP" if is_up else "DOWN"
            }
        }
        with open('market_summary.json', 'w') as f_json:
            json.dump(summary_json, f_json, indent=2)
        
        print("\nSummary written to files.")
    
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
