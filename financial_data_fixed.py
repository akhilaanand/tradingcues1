import yfinance as yf
import datetime
import json

def get_price_data(ticker):
    data = yf.download(ticker, period="2d", auto_adjust=True)
    if data.empty or len(data) < 2:
        return None, None, None
    latest = float(data['Close'].iloc[-1])
    previous = float(data['Close'].iloc[-2])
    change = latest - previous
    return latest, change, previous

def format_change(change, previous):
    percent = (change / previous) * 100 if previous != 0 else 0
    direction = "🟢" if change > 0 else "🔴"
    return direction, change, percent

def main():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    summary = f"*Trade setup for {today}*\n"
    summary += "--------------------------------------------------\n"

    # 1. VIX
    vix, vix_change, vix_prev = get_price_data('^VIX')
    if vix is not None:
        vix_dir, vix_abs_change, vix_pct = format_change(vix_change, vix_prev)
        arrow = "↑" if vix_change >= 0 else "↓"
        market_trend = "UP 🟢" if vix_change >= 0 else "DOWN 🔴"
        summary += f"*VIX*: {vix:.2f} {arrow} +{abs(vix_change):.2f} ({abs(vix_pct):.2f}%)\n"
        summary += f"Market Volatility is *{market_trend}*\n\n"

    # 2. Crude Oil
    crude, crude_change, crude_prev = get_price_data('CL=F')
    if crude is not None:
        crude_dir, crude_abs_change, crude_pct = format_change(crude_change, crude_prev)
        summary += f"*Crude Oil*: {crude:.2f}\n"
        summary += f"{crude_dir} by {abs(crude_change):.2f} points\n\n"

    try:
    crude = fetch_data('CL=F')
    crude_line = format_line("Crude Oil", crude['latest'], crude['previous'])
    summary_lines.append(crude_line)
except Exception as e:
    print(f"Crude Oil data fetch failed: {e}")

    # 3. Gold
    gold, gold_change, gold_prev = get_price_data('GC=F')
    if gold is not None:
        gold_dir, gold_abs_change, gold_pct = format_change(gold_change, gold_prev)
        summary += f"*Gold*: {gold:.2f}\n"
        summary += f"{gold_dir} by {abs(gold_change):.2f} points\n\n"
try:
    gold = fetch_data('GC=F')
    gold_line = format_line("Gold", gold['latest'], gold['previous'])
    summary_lines.append(gold_line)
except Exception as e:
    print(f"Gold data fetch failed: {e}")
    
    # 4. S&P 500
    spx, spx_change, spx_prev = get_price_data('^GSPC')
    if spx is not None:
        spx_dir, spx_abs_change, spx_pct = format_change(spx_change, spx_prev)
        spx_trend = "bullish 🟢" if spx_change > 0 else "bearish 🔴"
        summary += f"*S&P 500*: {spx:.2f} {spx_dir}\n"
        summary += f"S&P 500 looks *{spx_trend}*\n"

    # Print and save
    print(summary)
    with open('market_summary.txt', 'w') as f:
        f.write(summary)

    # Optional JSON output
    summary_json = {
        "date": today,
        "VIX": vix,
        "CrudeOil": crude,
        "Gold": gold,
        "S&P500": spx
    }
    with open('market_summary.json', 'w') as f_json:
        json.dump(summary_json, f_json, indent=2)

if __name__ == "__main__":
    main()
