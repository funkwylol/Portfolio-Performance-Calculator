from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()

    initial_portfolio = float(data["initialPortfolio"])
    risk = float(data["risk"]) / 100
    rr_ratio = float(data["riskRewardRatio"])
    trades_per_day = int(data["tradesPerDay"])
    trading_days = int(data["tradingDays"])
    num_sim = int(data["numSimulations"])
    win_prob = float(data["winProbability"]) / 100
    risk_free_rate = float(data["riskFreeRate"])

    all_results = []

    for _ in range(num_sim):
        portfolio = initial_portfolio
        for _ in range(trades_per_day):
            if np.random.rand() < win_prob:
                portfolio += portfolio * (rr_ratio * risk)
            else:
                portfolio -= portfolio * risk
        daily_return = ((portfolio - initial_portfolio) / initial_portfolio) * 100
        all_results.append(daily_return)

    avg_daily_return = np.mean(all_results)
    std_dev = np.std(all_results, ddof=1)
    sharpe_ratio = (avg_daily_return - (risk_free_rate / 252)) / std_dev
    estimated_annual_return = ( (1 + avg_daily_return/100)**trading_days - 1 ) * 100

    result = {
        "average": round(avg_daily_return, 2),
        "best": round(max(all_results), 2),
        "worst": round(min(all_results), 2),
        "sharpe": round(sharpe_ratio, 2),
        "stdDev": round(std_dev, 2),
        "annualReturn": round(estimated_annual_return, 2),
        "dailyResults": all_results
    }
    return jsonify(result)

@app.route("/risk_curve", methods=["POST"])
def risk_curve():
    data = request.get_json()
    initial_portfolio = float(data["initialPortfolio"])
    rr_ratio = float(data["riskRewardRatio"])
    trades_per_day = int(data["tradesPerDay"])
    num_sim = int(data["numSimulations"])
    win_prob = float(data["winProbability"]) / 100
    risk_free_rate = float(data["riskFreeRate"])

    risk_values = []
    sharpe_ratios = []

    for r in range(1, 21):  # 1% to 20%
        risk = r / 100
        all_results = []
        for _ in range(num_sim):
            portfolio = initial_portfolio
            for _ in range(trades_per_day):
                if np.random.rand() < win_prob:
                    portfolio += portfolio * (rr_ratio * risk)
                else:
                    portfolio -= portfolio * risk
            daily_return = ((portfolio - initial_portfolio) / initial_portfolio) * 100
            all_results.append(daily_return)

        avg_return = np.mean(all_results)
        std_dev = np.std(all_results, ddof=1)
        sharpe = (avg_return - (risk_free_rate / 252)) / std_dev if std_dev != 0 else 0

        risk_values.append(r)
        sharpe_ratios.append(round(sharpe, 2))

    return jsonify({"risk": risk_values, "sharpe": sharpe_ratios})


if __name__ == "__main__":
    app.run(debug=True)
