import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("FMP_API_KEY")

def get_today_earnings():
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={today}&to={today}&apikey={API_KEY}"
    res = requests.get(url)
    return res.json()

def analyze(report):
    try:
        symbol = report['symbol']
        eps = float(report.get('eps', 0))
        eps_est = float(report.get('epsEstimated', 0))
        rev = float(report.get('revenue', 0))
        rev_est = float(report.get('revenueEstimated', 0))
    except:
        return "보류", f"{symbol}: 데이터 부족"

    if eps > eps_est and rev > rev_est:
        return "매수", f"{symbol}: EPS, 매출 모두 서프라이즈"
    elif eps < eps_est and rev < rev_est:
        return "매도", f"{symbol}: EPS, 매출 모두 부진"
    else:
        return "보류", f"{symbol}: 혼합 결과"

def main():
    earnings = get_today_earnings()
    print(f"🔍 오늘 공시 기업 수: {len(earnings)}\n")
    for report in earnings:
        decision, reason = analyze(report)
        print(f"[{decision}] {reason}")

if __name__ == "__main__":
    main()