# -*- coding: utf-8 -*-
"""
Created on Tue May 02 19:23:37 2017

@author: user
"""

from flask import Flask
import requests
import json

URL = "https://nginx0.pncapix.com"
version = "/v1.0.0"
header_dict = {"Content-Type": "application/json", "Accept": "application/json", 'Authorization': "Bearer efa92a43-be7b-32ef-a6df-ef1831d4d9ca"}
print header_dict
app = Flask(__name__)

def login(username, password):
    creds = {}
    param = {}
    creds['username'] = username
    creds['password'] = password
    param['accountCredentials'] = creds
    response = httpPost(creds, 'security', 'login')
    return response.text
    
def httpPost(params, api, func):
    response = requests.post(URL + '/' + api + version + '/' + func, headers=header_dict, json=params)   
    return response
    
@app.route("/")
def hello():
    return login('mayduncan323', 'mayduncan323')


if __name__ == "__main__":
    app.run()
    