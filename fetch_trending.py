import requests
import json
from datetime import datetime
import os

SAVE_PATH = "trending_data.json"

def fetch_trending_data():
    url = "https://api.coingecko.com/api/v3/search/trending"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            result = res.json()["coins"]
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            data = []
            for i, coin in enumerate(result):
                item = coin['item']
                data.append({
                    "rank": i + 1,
                    "name": item['name'],
                    "symbol": item['symbol'],
                    "price_btc": item['price_btc'],
                    "timestamp": now
                })
            return now, data
        else:
            print(f"[ERROR] API 실패: {res.status_code}")
            return None, []
    except Exception as e:
        print(f"[ERROR] 예외 발생: {e}")
        return None, []

def save_data(now, data):
    if os.path.exists(SAVE_PATH):
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}
    else:
        all_data = {}

    all_data[now] = data
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"[{now}] 저장 완료")

if __name__ == "__main__":
    now, data = fetch_trending_data()
    if data:
        save_data(now, data)
