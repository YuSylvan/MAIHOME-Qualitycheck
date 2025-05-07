from flask import Flask, render_template, jsonify
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import api_call
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
app = Flask(__name__)

# 读取 JSON 资产数据
asset_list_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'asset_list_wo.json'))
assets = api_call.load_assets_from_json(asset_list_path)

# 设置时间范围
start_time = datetime.now(ZoneInfo("UTC")) - timedelta(hours=12)
end_time = datetime.now(ZoneInfo("UTC"))

# 设定阈值
thresholds_MAI = {
    'active_power': {'min': 0, 'max': 5000},
    'battery': {'min': 0, 'max': 100},
    'co2': {'min': 0, 'max': 5000},
    'current': {'min': 0, 'max': 1000},
    'humidity': {'min': 0, 'max': 100},
    'temperature': {'min': -20, 'max': 50},
    'setTemperature': {'min': -20, 'max': 50},
    'temperature.current': {'min': -20, 'max': 50},
    'temperature.set': {'min': -20, 'max': 50},
    'pressure': {'min': 900, 'max': 1100},
    'tvoc': {'min': 0, 'max': 1000},
}

# 运行 API 检测
df_results = api_call.check_import_data(assets, thresholds_MAI, start_time=start_time, end_time=end_time)

# 首页
@app.route("/")
def home():
    return render_template("index.html", tables=[df_results.to_html(classes='data')], titles=df_results.columns.values)

# API: 以 JSON 格式返回数据
@app.route("/api/results")
def get_results():
    return jsonify(df_results.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
