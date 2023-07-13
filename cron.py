from fetch import fetch_and_save_lsorders, fetch_last_order, get_customization
import time
from datetime import datetime, timedelta

while True:
    try:
        last_order_id = fetch_last_order()
        # fetch_and_save_lsorders(244670771)
        fetch_and_save_lsorders(last_order_id)
        get_customization()
        print("APP.PY", datetime.now())
        time.sleep(300)

    except KeyboardInterrupt:
        print("END OF LOOP")
        break
    except:
        print("SOMETHING WENT WRONG")
        break
