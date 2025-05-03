import json
import requests
import os
import sys
import numpy as np
import pandas as pd

# Helper function to make objects JSON serializable for Slack
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(JsonEncoder, self).default(obj)

def send_slack_message():
    try:
        # Check if the webhook URL is set
        webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        if not webhook_url:
            print("Error: SLACK_WEBHOOK_URL environment variable not set.")
            sys.exit(1)
            
        # Read the market summary
        if not os.path.exists('market_summary.txt'):
            print("Error: market_summary.txt not found. Run financial_data_fixed.py first.")
            sys.exit(1)
            
        with open('market_summary.txt', 'r') as f:
            summary = f.read()
        
        # Read market data for more structured information
        if os.path.exists('market_data.json'):
            with open('market_data.json', 'r') as f:
                market_data = json.load(f)
                
            date = market_data['date']
            data = market_data['data']
            
            # Create a more visually appealing message for Slack
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📊 Market Summary for {date}",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Market Indices*"
                    }
                }
            ]
            
            # Add indices
            indices_fields = []
            for name in ['S&P 500', 'Dow Jones', 'NASDAQ', 'VIX']:
                if name in data:
                    price = data[name]['price']
                    change = data[name]['change']
                    percent_change = data[name]['percent_change']
                    
                    if price != "N/A":
                        emoji = "🟢" if change >= 0 else "🔴"
                        change_sign = "+" if change >= 0 else ""
                        field_text = f"{emoji} *{name}*\n{price:,.2f} ({change_sign}{change:,.2f}, {change_sign}{percent_change:,.2f}%)"
                    else:
                        field_text = f"⚠️ *{name}*\nData not available"
                        
                    indices_fields.append({
                        "type": "mrkdwn",
                        "text": field_text
                    })
            
            # Add indices fields in pairs
            for i in range(0, len(indices_fields), 2):
                fields = indices_fields[i:i+2]
                blocks.append({
                    "type": "section",
                    "fields": fields
                })
            
            # Add stocks section header
            blocks.append({
                "type": "divider"
            })
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Major Stocks*"
                }
            })
            
            # Add stocks
            stocks_fields = []
            for name in ['Apple', 'Microsoft', 'Amazon', 'Google']:
                if name in data:
                    price = data[name]['price']
                    change = data[name]['change']
                    percent_change = data[name]['percent_change']
                    
                    if price != "N/A":
                        emoji = "🟢" if change >= 0 else "🔴"
                        change_sign = "+" if change >= 0 else ""
                        field_text = f"{emoji} *{name}*\n{price:,.2f} ({change_sign}{change:,.2f}, {change_sign}{percent_change:,.2f}%)"
                    else:
                        field_text = f"⚠️ *{name}*\nData not available"
                        
                    stocks_fields.append({
                        "type": "mrkdwn",
                        "text": field_text
                    })
            
            # Add stocks fields in pairs
            for i in range(0, len(stocks_fields), 2):
                fields = stocks_fields[i:i+2]
                blocks.append({
                    "type": "section",
                    "fields": fields
                })
                
            # Prepare the message payload
            payload = {
                "blocks": blocks
            }
            
            # Send the message using custom JSON encoder
            payload_json = json.dumps(payload, cls=JsonEncoder)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(webhook_url, data=payload_json, headers=headers)
            
            # Check if message was sent successfully
            if response.status_code == 200:
                print("Market summary sent to Slack successfully!")
            else:
                print(f"Failed to send message to Slack. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        else:
            # Fallback to simple text if no JSON data is available
            payload = {
                "text": summary
            }
            payload_json = json.dumps(payload, cls=JsonEncoder)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(webhook_url, data=payload_json, headers=headers)
            
            if response.status_code == 200:
                print("Market summary sent to Slack successfully!")
            else:
                print(f"Failed to send message to Slack. Status code: {response.status_code}")
                print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error sending Slack message: {e}")

if __name__ == "__main__":
    send_slack_message()
