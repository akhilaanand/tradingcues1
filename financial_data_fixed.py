import yfinance as yf
import datetime

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
        
        # Extract values as Python primitives
        try:
            latest_close = data['Close'].iloc[-1]
            previous_close = data['Close'].iloc[-2]
            
            # Explicitly convert to Python primitives
            latest_close_float = float(latest_close)
            previous_close_float = float(previous_close)
            
            print(f"\nVIX Latest Close: {latest_close_float:.2f}")
            print(f"VIX Previous Close: {previous_close_float:.2f}")
            
            # Simple up/down indicator
            change = latest_close_float - previous_close_float
            percent_change = (change / previous_close_float) * 100
            
            if change >= 0:
                direction = "UP ↑"
            else:
                direction = "DOWN ↓"
            
            print(f"\nMarket Volatility is {direction}")
            print(f"VIX Change: {change:.2f} ({percent_change:.2f}%)")
            
            # Write a simple summary to file
            summary = f"Market Summary for {today}\n"
            summary += "-" * 50 + "\n\n"
            summary += f"VIX: {latest_close_float:.2f} "
            
            if change >= 0:
                summary += f"↑ +{change:.2f} (+{percent_change:.2f}%)\n"
            else:
                summary += f"↓ {change:.2f} ({percent_change:.2f}%)\n"
                
            summary += f"\nMarket Volatility is {direction}\n"
            
            # Save the summary to a file
            with open('market_summary.txt', 'w') as f:
                f.write(summary)
                
            print("\nSummary written to market_summary.txt")
            
        except Exception as e:
            print(f"Error processing VIX data: {e}")
            
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
