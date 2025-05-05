import yfinance as yf
import datetime
import json

# Fetch financial data for a given ticker
def fetch_data(ticker):
    data = yf.download(ticker, period="2d")
    
    # Make sure data is available
    if data.empty or len(data) < 2:
        raise Exception(f"Insufficient data for {ticker}")
    
    latest = float(data['Close'].iloc[-1])
    previous = float(data['Close'].iloc[-2])
    
    return {"latest": latest, "previous": previous}

# Format the output for each data point
def format_line(name, latest, previous):
    change = latest - previous
    percent_change = (change / previous) * 100
    direction = "🟢" if change >= 0 else "🔴"
    trend = "bullish" if change >= 0 else "bearish"
    
    line = f"*{name}*: {latest:.2f} {direction}"
    line += f"\n{name} looks *{trend} {direction}*"
    line += f" by {abs(change):.2f} points ({percent_change:.2f}%)\n"
    
    return line

def main():
    try:
        # Get today's date
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        print(f"Trade setup for {today}")
        print("-" * 50)
        
        # Initialize the summary
        summary_lines = []
        
        # Fetch VIX data
        try:
            vix = fetch_data('^VIX')
            vix_line = format_line("VIX", vix['latest'], vix['previous'])
            summary_lines.append(vix_line)
        except Exception as e:
            print(f"VIX data fetch failed: {e}")
        
        # Fetch S&P 500 data
        try:
            sp500 = fetch_data('^GSPC')
            sp500_line = format_line("S&P 500", sp500['latest'], sp500['previous'])
            summary_lines.append(sp500_line)
        except Exception as e:
            print(f"S&P 500 data fetch failed: {e}")
        
        # Fetch Gold data
        try:
            gold = fetch_data('GC=F')
            gold_line = format_line("Gold", gold['latest'], gold['previous'])
            summary_lines.append(gold_line)
        except Exception as e:
            print(f"Gold data fetch failed: {e}")
        
        # Fetch Crude Oil data
        try:
            crude = fetch_data('CL=F')
            crude_line = format_line("Crude Oil", crude['latest'], crude['previous'])
            summary_lines.append(crude_line)
        except Exception as e:
            print(f"Crude Oil data fetch failed: {e}")
        
        # Print the summary
        summary = f"*Trade setup for {today}*\n"
        summary += "-" * 50 + "\n"
        summary += "\n".join(summary_lines)
        
        # Print summary to the console
        print(summary)
        
        # Save the summary to a text file
        with open('market_summary.txt', 'w') as f:
            f.write(summary)
        
        print("\nSummary written to market_summary.txt")
        
        # Save the summary as JSON
        summary_json = {
            "date": today,
            "data": summary_lines
        }
        with open('trade_setup_summary.json', 'w') as f_json:
            json.dump(summary_json, f_json, indent=2)
        
        print("JSON summary written to trade_setup_summary.json")
    
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
