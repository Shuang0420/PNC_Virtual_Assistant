# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
#import web

# sample username and password
USERNAME = 'mayduncan323'
PASSWORD = 'mayduncan323'
URL = "https://nginx0.pncapix.com"
version = "/v1.0.0"
header_dict = {"Content-Type": "application/json", "Accept": "application/json", 'Authorization': "Bearer efa92a43-be7b-32ef-a6df-ef1831d4d9ca"}
account_types = {"STANDARD_SAVINGS": 1, "STANDARD_CHECKING": 2, "PNC_CORE_VISA_CREDIT_CARD": 6, "VIRTUAL_WALLET_SPEND": 15, "VIRTUAL_WALLET_RESERVE": 16,
"VIRTUAL_WALLET_GROWTH": 17}

pnc_api_token = ''

# define Flask app
app = Flask(__name__)
# give basic endpoint, can be flask skill/program endpoint
ask = Ask(app, "/pnc_assistant")


# get answer to frequent asked questions
# hard code
def getFAQ():
    pass



# set home url path
@app.route('/pnc_assistant')
def homepage():
    return 'welcome to pnc assistant'


@ask.launch
def start_skill():
    # it will say
    welcome_message = 'Hello there, what can I do for you?'
    # question expect response
    return question(welcome_message)



@ask.intent("BalanceIntent", mapping={'account_type': 'AccountType'})
def checkBalance(account_type):
    # bal = web.getAccount()
    bal = 999
    # session.attributes['query_type'] = 'balance'
    if account_type:
        bal = 111
    else:
        account_type = 'standard checking'
    stat = ' '.join(['Your', account_type, 'balance is'])
    return statement(' '.join([stat, ' . ', str(bal), ' . ', 'anything else I can help you']))


@ask.intent("TransactionIntent", mapping={'time_span': 'TimeSpan'})
def checkTransaction(time_span):
    # bal = web.getAccount()
    bal = 999
    # session.attributes['query_type'] = 'balance'
    if time_span:
        bal = 111
    else:
        time_span = 'week'
    stat = ' '.join(['You spent . ', str(bal), 'last',time_span, ' . ', 'anything else I can help you'])
    print bal, time_span, stat
    return statement(stat)





@ask.intent("FAQIntent")
def FAQ():
    pass

# handle user input yes or no response
# user input is intent
@ask.intent("YesIntent")
def share_headlines():
    # grab the headline
    headlines = get_headlines()
    headline_msg = 'The current world news headlines are {}'.format(headlines)
    # statement tell you sth
    return statement(headline_msg)


@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)



def alexa_stop_cancel():
  if session.new:
    return statement("how can I help you")
  else:
    return statement("")

# Handle the AMAZON.StopIntent intent.
@ask.intent('AMAZON.StopIntent')
def alexa_stop():
  return alexa_stop_cancel()


# Handle the AMAZON.CancelIntent intent.
@ask.intent('AMAZON.CancelIntent')
def alexa_cancel():
  return alexa_stop_cancel()


# Handle the AMAZON.NoIntent intent.
@ask.intent('AMAZON.NoIntent')
def alexa_no():
  return alexa_stop_cancel()


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


if __name__ == '__main__':
    # initalize pnc_api_token
    pnc_api_token = login(USERNAME, PASSWORD)
    app.run(debug=True)
