import yfinance as yf
import datetime
import json
import os

def get_market_data():
    try:
        # Get today's date
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # Define major indices to track
        indices = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^VIX': 'VIX'
        }
        
        market_data = {}
        
        # Get data for each index
        for symbol, name in indices.items():
            try:
                data = yf.download(symbol, period="2d")
                
                # Make sure we have data and at least 2 rows
                if data.empty or len(data) < 2:
                    print(f"Warning: Insufficient data for {name} ({symbol})")
                    market_data[name] = {
                        "price": "N/A",
                        "change": "N/A",
                        "percent_change": "N/A"
                    }
                    continue
                    
                # Get the latest closing price - convert to Python primitive types explicitly
                latest_close = float(data['Close'].iloc[-1])
                previous_close = float(data['Close'].iloc[-2])
                
                # Calculate the change
                change = float(latest_close - previous_close)
                percent_change = float((change / previous_close) * 100)
                
                market_data[name] = {
                    "price": float(round(latest_close, 2)),
                    "change": float(round(change, 2)),
                    "percent_change": float(round(percent_change, 2))
                }
            except Exception as e:
                print(f"Error processing {name}: {e}")
                market_data[name] = {
                    "price": "N/A",
                    "change": "N/A",
                    "percent_change": "N/A"
                }
        
        # Let's add a few major stocks as well
        stocks = {
            'AAPL': 'Apple',
            'MSFT': 'Microsoft',
            'AMZN': 'Amazon',
            'GOOGL': 'Google'
        }
        
        for symbol, name in stocks.items():
            try:
                data = yf.download(symbol, period="2d")
                
                # Make sure we have data and at least 2 rows
                if data.empty or len(data) < 2:
                    print(f"Warning: Insufficient data for {name} ({symbol})")
                    market_data[name] = {
                        "price": "N/A",
                        "change": "N/A",
                        "percent_change": "N/A"
                    }
                    continue
                    
                # Get the latest closing price - convert to Python primitive types explicitly
                latest_close = float(data['Close'].iloc[-1])
                previous_close = float(data['Close'].iloc[-2])
                
                # Calculate the change
                change = float(latest_close - previous_close)
                percent_change = float((change / previous_close) * 100)
                
                market_data[name] = {
                    "price": float(round(latest_close, 2)),
                    "change": float(round(change, 2)),
                    "percent_change": float(round(percent_change, 2))
                }
            except Exception as e:
                print(f"Error processing {name}: {e}")
                market_data[name] = {
                    "price": "N/A",
                    "change": "N/A",
                    "percent_change": "N/A"
                }
        
        # Create serializable data structure
        result = {"date": today, "data": market_data}
        
        # Debug output to help diagnose any issues
        print(f"Market data structure: {type(result)}")
        for key, value in market_data.items():
            print(f"{key}: {type(value['price'])}, {type(value['change'])}, {type(value['percent_change'])}")
        
        # Save the market data to a JSON file - use strict=False to handle NaN values
        with open('market_data.json', 'w') as f:
            json.dump(result, f, indent=4)
            
        return result
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

def format_market_summary(market_data):
    if not market_data:
        return "Failed to fetch market data."
    
    try:
        date = market_data['date']
        data = market_data['data']
        
        summary = f"Market Summary for {date}\n"
        summary += "-" * 50 + "\n\n"
        
        # Add indices data
        summary += "Market Indices:\n"
        for name in ['S&P 500', 'Dow Jones', 'NASDAQ', 'VIX']:
            if name in data:
                price = data[name]['price']
                change = data[name]['change']
                percent_change = data[name]['percent_change']
                
                if price != "N/A":
                    summary += f"{name}: {price:,.2f} "
                    if isinstance(change, (int, float)) and change >= 0:
                        summary += f"↑ +{change:,.2f} (+{percent_change:,.2f}%)\n"
                    else:
                        summary += f"↓ {change:,.2f} ({percent_change:,.2f}%)\n"
                else:
                    summary += f"{name}: Data not available\n"
        
        # Add major stocks data
        summary += "\nMajor Stocks:\n"
        for name in ['Apple', 'Microsoft', 'Amazon', 'Google']:
            if name in data:
                price = data[name]['price']
                change = data[name]['change']
                percent_change = data[name]['percent_change']
                
                if price != "N/A":
                    summary += f"{name}: {price:,.2f} "
                    if isinstance(change, (int, float)) and change >= 0:
                        summary += f"↑ +{change:,.2f} (+{percent_change:,.2f}%)\n"
                    else:
                        summary += f"↓ {change:,.2f} ({percent_change:,.2f}%)\n"
                else:
                    summary += f"{name}: Data not available\n"
        
        return summary
    except Exception as e:
        print(f"Error formatting market summary: {e}")
        return "Error formatting market summary."

def main():
    # Get market data
    market_data = get_market_data()
    
    # Format and display market summary
    summary = format_market_summary(market_data)
    print(summary)
    
    # Save the summary to a file
    with open('market_summary.txt', 'w') as f:
        f.write(summary)

if __name__ == "__main__":
    main()
