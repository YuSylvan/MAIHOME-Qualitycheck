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
db_manager = None
df_results = api_call.check_import_data(assets, db_manager, start_time=start_time, end_time=end_time)

print(df_results)
