import yfinance as yf
import pandas as pd
import datetime
import json
import os
import numpy as np

# Helper function to make objects JSON serializable
def convert_to_serializable(obj):
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

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
                
            # Get the latest closing price - ensure we convert to native Python float
            latest_close = float(data['Close'].iloc[-1])
            previous_close = float(data['Close'].iloc[-2])
            
            # Calculate the change
            change = latest_close - previous_close
            percent_change = (change / previous_close) * 100
            
            market_data[name] = {
                "price": round(latest_close, 2),
                "change": round(change, 2),
                "percent_change": round(percent_change, 2)
            }
        
        # Let's add a few major stocks as well
        stocks = {
            'AAPL': 'Apple',
            'MSFT': 'Microsoft',
            'AMZN': 'Amazon',
            'GOOGL': 'Google'
        }
        
        for symbol, name in stocks.items():
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
                
            # Get the latest closing price - ensure we convert to native Python float
            latest_close = float(data['Close'].iloc[-1])
            previous_close = float(data['Close'].iloc[-2])
            
            # Calculate the change
            change = latest_close - previous_close
            percent_change = (change / previous_close) * 100
            
            market_data[name] = {
                "price": round(latest_close, 2),
                "change": round(change, 2),
                "percent_change": round(percent_change, 2)
            }
        
        # Create serializable data structure
        result = {"date": today, "data": market_data}
        
        # Save the market data to a JSON file
        with open('market_data.json', 'w') as f:
            json.dump(result, f, indent=4, default=convert_to_serializable)
            
        return result
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return None

def format_market_summary(market_data):
    if not market_data:
        return "Failed to fetch market data."
    
    # Defensive programming - make sure we have valid data
    try:
        date = market_data['date']
        data = market_data['data']
    except (TypeError, KeyError):
        return "Failed to parse market data properly."
    
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
                if change >= 0:
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
                if change >= 0:
                    summary += f"↑ +{change:,.2f} (+{percent_change:,.2f}%)\n"
                else:
                    summary += f"↓ {change:,.2f} ({percent_change:,.2f}%)\n"
            else:
                summary += f"{name}: Data not available\n"
    
    return summary

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
