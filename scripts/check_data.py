import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import api_call
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo



asset_list_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'asset_list_wo.json'))
assets = api_call.load_assets_from_json(asset_list_path)

# Load the asset list
start_time = datetime.now(ZoneInfo("UTC")) - timedelta(hours=12)
end_time = datetime.now(ZoneInfo("UTC"))
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
        'tvoc' : {'min': 0, 'max': 1000},
    }
df_results = api_call.check_import_data(assets, thresholds_MAI, start_time=start_time, end_time=end_time)

