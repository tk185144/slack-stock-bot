import datetime
import json
import pandas
import requests
import yfinance as yf


def get_quarter_start(date):
    if date.month < 4:
        return datetime.date(date.year - 1, 12, 31)
    elif date.month < 7:
        return datetime.date(date.year, 3, 31)
    elif date.month < 10:
        return datetime.date(date.year, 6, 30)
    return datetime.date(date.year, 9, 30)


block = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "NCR Corporation Employee Stock Pruchase Plan(ESPP) Details"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Temp"
            }
        }
    ]
}

webhooks = [""]


def post_details(request):
    message = ""

    price = yf.Ticker("NCR").history(period="1d")
    current_price = round(pandas.DataFrame(price).iloc[0]["Close"], 2)
    message += "Current Price: $" + str(current_price) + "\n"

    today = datetime.date.today()
    qStart = get_quarter_start(today)

    price = yf.Ticker("NCR").history(period="1d", start=qStart, end=today)
    start_price = round(pandas.DataFrame(price).iloc[0]["Close"], 2)
    message += "Quarter Start Price: $" + str(start_price) + "\n"

    minimum = min(start_price, current_price)
    message += "Min: $" + str(minimum) + "\n"

    discount_price = round(minimum * .85, 2)
    message += "15% Discount Price: $" + str(discount_price) + "\n"

    diff = round(current_price - discount_price, 2)
    message += "Difference: $" + str(diff) + "\n"

    roi = 0.0
    if current_price < start_price:
        roi = round(diff * 100 / current_price, 2)
    else:
        roi = round(diff * 100 / discount_price, 2)
    message += "\n" + "ROI: " + str(roi) + "%"

    block["blocks"][1]["text"]["text"] = message

    print(block)

    # Post to Slack
    for wh in webhooks:
        r = requests.post(wh, data=json.dumps(block, indent=4))

    return "OK"

