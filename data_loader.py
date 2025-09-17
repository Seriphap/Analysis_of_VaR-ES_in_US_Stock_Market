import requests
import pandas as pd
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_price_data(symbol, interval, api_key):
    if interval == "Daily":
        function = "TIME_SERIES_DAILY"
        key_name = "Time Series (Daily)"
    elif interval == "Weekly":
        function = "TIME_SERIES_WEEKLY"
        key_name = "Weekly Time Series"
    elif interval == "Monthly":
        function = "TIME_SERIES_MONTHLY"
        key_name = "Monthly Time Series"
    else:
        raise ValueError("Unsupported interval")
    
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize=full&apikey={api_key}"
    r = requests.get(url, verify=False)
    data = r.json()
    #with open("data/query.json", 'r') as f:
    #    data = json.load(f)

    time_series = data.get(key_name, {})
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume",
    })
    
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


    return df


