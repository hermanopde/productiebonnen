from pymongo import MongoClient
from dotenv import dotenv_values
import datetime
from flask import Flask, redirect, url_for, render_template
from routes import order_pages, user_pages
from fetch import fetch_and_save_lsorders, fetch_last_order, get_customization
import time
from datetime import datetime
config = dotenv_values(".env")


app = Flask(__name__)

app.register_blueprint(order_pages, url_prefix="/orders")
app.register_blueprint(user_pages, url_prefix="/auth")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    # app.run(debug=True)
    while True:
        try:
            last_order_id = fetch_last_order()
            fetch_and_save_lsorders(243949398)
            # fetch_and_save_lsorders(last_order_id)
            get_customization()
            print(datetime.now())
            time.sleep(300)

        except KeyboardInterrupt:
            print("END OF LOOP")
            break
        except:
            print("SOMETHING WENT WRONG")
            break
