from fetch import fetch_and_save_lsorders, fetch_last_order, get_customization
import time
from datetime import datetime, timedelta

last_order_id = fetch_last_order()
fetch_and_save_lsorders(250160719)
# fetch_and_save_lsorders(last_order_id)
get_customization()
print("APP.PY", datetime.now())
