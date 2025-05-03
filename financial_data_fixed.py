import yfinance as yf
import datetime
import json

def main():
    try:
        # Get today's date
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print(f"Market Summary for {today}")
        print("-" * 50)
        
        # Just get VIX data
        print("Fetching VIX data...")
        data = yf.download('^VIX', period="2d")
        
        # Make sure we have data
        if data.empty or len(data) < 2:
            print("Warning: Insufficient VIX data")
            return
        
        # Print the raw data to help debug
        print("\nRaw data:")
        print(data.tail(2))
        
        # Extract and convert values
        latest_close = float(data['Close'].iloc[-1])
        previous_close = float(data['Close'].iloc[-2])
        
        print(f"\nVIX Latest Close: {latest_close:.2f}")
        print(f"VIX Previous Close: {previous_close:.2f}")
        
        change = latest_close - previous_close
        percent_change = (change / previous_close) * 100
        direction = "UP ↑" if change >= 0 else "DOWN ↓"
        
        print(f"\nMarket Volatility is {direction}")
        print(f"VIX Change: {change:.2f} ({percent_change:.2f}%)")
        
        # Build string summary
        summary_text = f"Market Summary for {today}\n"
        summary_text += "-" * 50 + "\n\n"
        summary_text += f"VIX: {latest_close:.2f} "
        if change >= 0:
            summary_text += f"↑ +{change:.2f} (+{percent_change:.2f}%)\n"
        else:
            summary_text += f"↓ {change:.2f} ({percent_change:.2f}%)\n"
        summary_text += f"\nMarket Volatility is {direction}\n"
        
        with open('market_summary.txt', 'w') as f:
            f.write(summary_text)
        
        print("\nSummary written to market_summary.txt")
        
        # Build JSON-safe summary
        summary_json = {
            "date": today,
            "VIX": {
                "latest_close": latest_close,
                "previous_close": previous_close,
                "change": round(change, 2),
                "percent_change": round(percent_change, 2),
                "direction": direction
            }
        }
        
        with open('market_summary.json', 'w') as f_json:
            json.dump(summary_json, f_json, indent=2)
        
        print("JSON summary written to market_summary.json")
    
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
