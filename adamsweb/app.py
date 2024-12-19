import flask
from flask import *

app = Flask(__name__)
print(__name__)
# set secret key to secure your session/make it unique
app.secret_key = "AW_r%@jN*HU4AW_r%@jN*HU4AW_r%@jN*HU4"
# Decorate your app with features
# http://127.0.0.1:5000/home

import pymysql

@app.route('/')
def home():
    # Establish a dbase connection
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='DemoClassDB')


    # SQL 1  - Smartphones
    sql1 = "SELECT * FROM products where product_category = 'Smartphones'"
    # Cursor - Used to run/execute above SQL
    cursor = connection.cursor()
    # Execute SQL
    cursor.execute(sql1)
    # Fetch Rows
    smartphones = cursor.fetchall()

    # SQL 2  - Detergents
    sql2 = "SELECT * FROM products where product_category = 'x'"

    # Execute SQL
    cursor.execute(sql2)
    # Fetch Rows
    detergents = cursor.fetchall()

    return render_template('index.html', detergents=detergents,
                           smartphones=smartphones)


import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/mpesa_payment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "5057335"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "5057335",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "5057335",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href="/" class="btn btn-dark btn-sm">Back to Products</a>'


app.run(debug)
