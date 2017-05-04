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
mccCode_dict = {"Drug": 5912, "Pharmacies": 5912, "Drug Store": 5912, "Medicine": 5912, "Auto Rental": 3351, "Auto": 3351, "Car Rent": 3351, "Fast Food Restaurants": 5814, "Fast Food": 5814, "Book Stores": 5942, "Book": 5942, "Other": 9999}
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
    
def getTransactionAmount(timespan):
    now = datetime.datetime.now() - datetime.timedelta(days=190)
    if timespan == 'week':
        start = now.date() - datetime.timedelta(days=datetime.datetime.today().isoweekday())
        start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        return getTransactionByDate(pnc_api_token, start, now)
    elif timespan == 'month':
        start = datetime.datetime(now.year, now.month, 1)
        start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z';
        return getTransactionByDate(pnc_api_token, start, now)
    elif timespan == 'year':
        start = datetime.datetime(now.year, 1, 1)
        start = start.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'
        return getTransactionByDate(pnc_api_token, start, now)
        
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
    
def getTransactionByDate(pnc_api_token, start, end):
    header = dict(header_dict)
    param = {}
   
    param['size'] = 10
    header['X-Authorization'] = 'Bearer ' + pnc_api_token
    param['startDate'] = start
    param['endDate'] = end
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
    
@app.route("/")
def hello():
    
    pnc_api_token = login('mayduncan323', 'mayduncan323')
    print pnc_api_token
    #return str(getTransactionByCat('Book'))
    return str(getAccounts(pnc_api_token))
    #return str(getTransactionAmount('week'))
    #return str(getTransactionByDate(pnc_api_token, 0, 10, '2017-01-01T00:00:00.000Z', '2017-05-04T13:13:51.048Z'))
    #return getAccounts(pnc_api_token, 0, 10)
    #return "Hello"


if __name__ == "__main__":
    #pnc_api_token = login('mayduncan323', 'mayduncan323')['token']
    app.run()
    