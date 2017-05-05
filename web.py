# -*- coding: utf-8 -*-
"""
Created on Tue May 02 19:23:37 2017

@author: user
"""

from flask import Flask
import requests
import json
import datetime

URL = "https://nginx0.pncapix.com"
version = "/v1.0.0"
header_dict = {"Content-Type": "application/json", "Accept": "application/json", 'Authorization': "Bearer efa92a43-be7b-32ef-a6df-ef1831d4d9ca"}
mccCode_dict = {"drug": 5912, "pharmacies": 5912, "drug store": 5912, "medicine": 5912, "auto rental": 3351, "auto": 3351, "car rent": 3351, "fast food restaurants": 5814, "fast food": 5814, "book stores": 5942, "book": 5942, "other": 9999}
#pnc_api_token = ''

app = Flask(__name__)

def login(username, password):
    creds = {}
    param = {}
    creds['username'] = username
    creds['password'] = password
    param['accountCredentials'] = creds
    response = httpPost(creds, 'security', 'login')
    return response.json()['token']

def getAccounts(pnc_api_token):
    header = dict(header_dict)
    param = {}

    param['size'] = 10
    header['X-Authorization'] = 'Bearer ' + pnc_api_token
    page = 0
    accounts = {}
    while True:
        param['page'] = page
        response = httpGet(header, param, 'accounts', 'account').json()['content']
        if len(response) == 0: break
        page = page + 1
        for account in response:
            accounts[account['accountType']['accountType']] = account['balance']
    return accounts

def getTransactionAmount(pnc_api_token, timespan=None, category=None):
    now = datetime.datetime.now() - datetime.timedelta(days=190)
    if timespan is None:
        timespan = 'today'
    if timespan == 'today':
        start = datetime.datetime(now.year, now.month, now.day)
        start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        return getTransactionByDateAndCat(pnc_api_token, start, now, category)
    elif timespan == 'week':
        start = now.date() - datetime.timedelta(days=datetime.datetime.today().isoweekday())
        start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        return getTransactionByDateAndCat(pnc_api_token, start, now, category)
    elif timespan == 'month':
        start = datetime.datetime(now.year, now.month, 1)
        start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z';
        return getTransactionByDateAndCat(pnc_api_token, start, now, category)
    elif timespan == 'year':
        start = datetime.datetime(now.year, 1, 1)
        start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        return getTransactionByDateAndCat(pnc_api_token, start, now, category)
    else:
        return None


def getTransactionByCat(pnc_api_token, category):
    header = dict(header_dict)
    param = {}

    param['size'] = 10
    header['X-Authorization'] = 'Bearer ' + pnc_api_token
    param['mccCode'] = mccCode_dict[category]

    page = 0
    total = 0.0
    while True:
        param['page'] = page
        transactions = httpGet(header, param, 'transactions', 'transaction/find').json()['content']
        if len(transactions) == 0: break
        page = page + 1
        print category, len(transactions)

        for trans in transactions:
            if not trans['transactionType']['accountType'] == 'DEPOSIT':
                total += trans['amount']
                print trans['mccCode']['editedDescription']
            else:
                pass
    return total

def getTransactionByDateAndCat(pnc_api_token, start, end, category=None):
    header = dict(header_dict)
    param = {}

    param['size'] = 10
    header['X-Authorization'] = 'Bearer ' + pnc_api_token
    param['startDate'] = start
    param['endDate'] = end
    if category is not None:
        category = category.lower()
        if category not in mccCode_dict:
            return None
        param['mccCode'] = mccCode_dict[category]
    page = 0
    total = 0.0
    while True:
        param['page'] = page
        transactions = httpGet(header, param, 'transactions', 'transaction/find').json()['content']
        if len(transactions) == 0: break
        page = page + 1
        print start, end, len(transactions)

        for trans in transactions:
            if not trans['transactionType']['accountType'] == 'DEPOSIT':
                total += trans['amount']
                print trans['transactionDate']
            else:
                pass
    return total

def httpGet(header, params, api, func):
    response = requests.get(URL + '/' + api + version + '/' + func, headers=header, params=params)
    return response

def httpPost(params, api, func):
    response = requests.post(URL + '/' + api + version + '/' + func, headers=header_dict, json=params)
    return response

# @app.route("/")
# def hello():
#
#     pnc_api_token = login('mayduncan323', 'mayduncan323')
#     print pnc_api_token
#     #return str(getTransactionByCat('Book'))
#     #return str(getAccounts(pnc_api_token))
#     return str(getTransactionAmount(pnc_api_token, timespan='week', category='Book'))
#     #return str(getTransactionByDate(pnc_api_token, 0, 10, '2017-01-01T00:00:00.000Z', '2017-05-04T13:13:51.048Z'))
#     #return getAccounts(pnc_api_token, 0, 10)
#     #return "Hello"
#
#
# if __name__ == "__main__":
#     #pnc_api_token = login('mayduncan323', 'mayduncan323')['token']
#     s = requests.session()
#     s.keep_alive = False
#     app.run()
