import requests
import os
import sys

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
            
        with open('trade_setup_summary.txt', 'r') as f:
            summary = f.read()
        
        # Most basic possible message payload
        payload = {
            "text": summary
        }
        
        # Send as plain text
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 200:
            print("Market summary sent to Slack successfully!")
        else:
            print(f"Failed to send message to Slack. Status code: {response.status_code}")
            print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error sending Slack message: {e}")

if __name__ == "__main__":
    send_slack_message()
