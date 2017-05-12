# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import web
from socialMediaHelper import tweet
from creditBooster import creditTests
import unirest

# sample username and password
USERNAME = 'mayduncan323'
PASSWORD = 'mayduncan323'
URL = "https://nginx0.pncapix.com"
version = "/v1.0.0"
header_dict = {"Content-Type": "application/json", "Accept": "application/json", 'Authorization': "Bearer efa92a43-be7b-32ef-a6df-ef1831d4d9ca"}
account_types = {"savings":"STANDARD_SAVINGS", "checking":"STANDARD_CHECKING", "credit":"PNC_CORE_VISA_CREDIT_CARD", "virtual wallet spend":"VIRTUAL_WALLET_SPEND", "virtual wallet reserve":"VIRTUAL_WALLET_RESERVE",
"virtual wallet growth":"VIRTUAL_WALLET_GROWTH"}

pnc_api_token = ''

# define Flask app
app = Flask(__name__)
# give basic endpoint, can be flask skill/program endpoint
ask = Ask(app, "/pnc_assistant")

transaction_type_global = ''

# tweet('testing tweet')


# set home url path
@app.route('/pnc_assistant')
def homepage():
    return 'welcome to pnc assistant'


@ask.launch
def start_skill():
    # it will say
    welcome_message = 'Hello there, just a quick reminder . You have a car loan payment of 3000 dollars due this Saturday . . what can I do for you today?'
    # welcome_message = 'Hello there.'
    # question expect response
    pass_parameter('none')
    pass_response(welcome_message)
    return question(welcome_message)


@ask.intent("BalanceIntent", mapping={'account_type': 'AccountType'})
def checkBalance(account_type):
    bal = web.getAccounts(pnc_api_token)
    #bal = 999
    # session.attributes['query_type'] = 'balance'
    if account_type:
        bal = bal[account_types[account_type]]
    else:
        bal = bal['STANDARD_CHECKING']
        account_type = 'standard checking'
    stat = ' '.join(['Your', account_type, 'balance is', ' . ', str(bal), ' . ', 'anything else I can help you'])
    pass_parameter(account_type)
    pass_response(stat)
    return question(stat).reprompt("I didn't get that. Can you say it again?")



@ask.intent("TransactionIntent", mapping={'time_span': 'TimeSpan', 'transaction_type': 'TransactionCategory'})
def checkTransaction(time_span, transaction_type):
    # session.attributes['query_type'] = 'balance'
    bal = web.getTransactionAmount(pnc_api_token, time_span, transaction_type)
    if not bal:
        return question("Sorry I didn't get it. Can you try again?")
    if not time_span and not transaction_type:
        stat = ' '.join(['You spent . ', str(bal), 'today', ' . ', 'anything else I can help you'])
    elif not transaction_type:
        stat = ' '.join(['You spent . ', str(bal), 'last', time_span, ' . ', 'anything else I can help you'])
    elif not time_span:
        stat = ' '.join(['You spent . ', str(bal), 'today on', transaction_type, ' . ', 'anything else I can help you'])
    else:
        stat = ' '.join(['You spent . ', str(bal), 'last', time_span, 'on', transaction_type, ' . ', 'anything else I can help you'])
    pass_parameter(time_span + '\t' + transaction_type)
    pass_response(stat)
    return question(stat).reprompt("I didn't get that. Can you say it again?")



@ask.intent("LostCardIntent")
def lost_card_handler():
    answer = 'If your card has been lost or stolen, contact us immediately at one of the following phone numbers. . Personal Debit Cards . 1 888 762 2265 . Virtual Wallet . 1 800 352 2255'
    stat = ' '.join([answer, ' . ', 'anything else I can help you'])
    pass_parameter('none')
    pass_response(stat)
    return question(stat).reprompt("I didn't get that. Can you say it again?")


@ask.intent("AdviceIntent")
def adviceWealth():
    # get balance from saving account
    bal = 5000

    # interest rate for saving is constant for all balance
    # ref https://apps.pnc.com/rates/servlet/DepositRatesSearch?productGroup=mmarket
    ir = 0.0001

    # interest rate for performance checking in money market
    # ref https://apps.pnc.com/rates/servlet/DepositRatesSearch?productGroup=mmarket
    if bal < 10000:
        mmir = 0.0025
    elif bal < 25000:
        mmir = 0.0027
    elif bal < 50000:
        mmir = 0.0030
    elif bal < 100000:
        mmir = 0.0032
    else:
        mmir = 0.0035

    ie = ir * bal
    mmie = mmir * bal

    stat = ' '.join(['You have a healthy portfolio of ', str(bal), 'dollars in saving. You are getting', str(ie), 'interest earnings every year. You can do even greater with money market and your interest earning will be', str(mmie), 'dollars per year. . anything else I can help you'])
    pass_parameter('none')
    pass_response(stat)
    return question(stat).reprompt("I didn't get that. Can you say it again?")


@ask.intent("BudgetIntent", mapping={'budget_amount': 'BudgetAmount', 'transaction_type': 'TransactionCategory'})
def setBudget(budget_amount, transaction_type):
    if budget_amount and transaction_type:
        answer = 'ok. budget for' + transaction_type + 'is set succesfully'
    # elif not transaction_type:
    #     return question('what is the amount')#.prompt()
    stat = ' '.join([answer, ' . ', 'anything else I can help you'])
    pass_parameter(str(budget_amount) + '\t' + transaction_type)
    pass_response(stat)
    return question(stat).reprompt("what is the amount?")


def alexa_stop_cancel():
    if session.new:
        return statement("how can I help you")
    else:
        return statement("bye bye")


# Handle the AMAZON.StopIntent intent.
@ask.intent('AMAZON.StopIntent')
def alexa_stop():
    return alexa_stop_cancel()


# Handle the AMAZON.CancelIntent intent.
@ask.intent('AMAZON.CancelIntent')
def alexa_cancel():
    return alexa_stop_cancel()


@ask.intent("BudgetAddAmountIntent", mapping={'budget_amount': 'BudgetAmount'})
def setBudget(budget_amount):
    global transaction_type_global
    if budget_amount and transaction_type_global:
        web.setBudget(pnc_api_token, budget_amount, transaction_type_global)
        # PNC api to create budget
        answer = 'You created a budget with ${} for healthcare successfully. Do you want to \
                    share the budget plan on Twitter?'.format(budget_amount, transaction_type_global)
        repromt_msg = "Sorry, could you please say the budget amount again?"
        session.attributes['budget_amount'] = budget_amount
        session.attributes['transaction_type_global'] = transaction_type_global
        transaction_type_global = ''
        pass_parameter(budget_amount)
        pass_response(answer)
        return question(answer).reprompt(repromt_msg)
    # if not transaction_type_global:
    #     return question('which category you want to add')


@ask.intent("BudgetTriggerIntent")
def triggerBudget():
    stat = 'which category you want to add the budget'
    pass_parameter('none')
    pass_response(stat)
    return question(stat)


@ask.intent("BudgetAddCategoryIntent", mapping={'transaction_type': 'TransactionCategory'})
def addCatBudget(transaction_type):
    global transaction_type_global
    transaction_type_global = transaction_type
    question_phrase = "Actually, according to people in similar financial situation in pittsburgh, I suggest you to set {} dollars for {}. What amount do you want to set?".format(500, transaction_type)
    pass_parameter(transaction_type)
    pass_response(question_phrase)
    return question(question_phrase)


# handle user input yes or no response
# user input is intent
@ask.intent("MyYesIntent")
def twitter_share():
    print 'SHARE'
    budget_amount = session.attributes['budget_amount']
    transaction_type_global = session.attributes['transaction_type_global']
    print 'AMO', budget_amount, 'TYPE', transaction_type_global
    tweet('I have set a ${} budget for {} in my PNC account through cute Alexa PNC Assistant'.format(budget_amount, transaction_type_global))
    stat = 'You have set a ${} budget for {} in your PNC account through cute Alexa PNC Assistant . anything else I can help you'.format(budget_amount, transaction_type_global)
    pass_parameter('none')
    pass_response(stat)
    return question(stat)


@ask.intent("MyNoIntent")
def no_intent():
    stat = 'okay. what else can i do for you'
    pass_parameter('none')
    pass_response(stat)
    return question(stat)


def pass_response(text):
    DATA = {}
    DATA['text'] = text
    print DATA
    # r = unirest.post('https://apifestdemo.herokuapp.com/demo/AlexaResponse', headers={"Accept": "application/json"}, json=json.dumps(DATA))
    url = "https://apifestdemo.herokuapp.com/demo/AlexaResponse"
    payload = json.dumps(DATA)
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "732e5426-fe44-2c9b-c626-429ec6fbe487"
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    # r = requests.post('https://apifestdemo.herokuapp.com/demo/AlexaResponse', json=DATA)
    # print r


def pass_parameter(text):
    DATA = {}
    DATA['text'] = text
    DATA['user'] = 'awesome'
    print DATA
    # r = unirest.post('https://apifestdemo.herokuapp.com/demo/userRequest', headers={"Accept": "application/json"}, json=json.dumps(DATA))
    url = "https://apifestdemo.herokuapp.com/demo/AlexaResponse"
    # payload = "{\n\t\"user\": \"user\",\n\t\"text\": \"PM said I need to get some better test data to test it.\"\n}"
    payload = json.dumps(DATA)
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "732e5426-fe44-2c9b-c626-429ec6fbe487"
    }
    response = requests.request("POST", url, data=payload, headers=headers)



@ask.intent("BudgetCheckIntent", mapping={'category': 'TransactionCategory'})
def checkBudget(category):
    print 'category',category
    if category:
        try:
            budget = web.getBudget(pnc_api_token, category)
        except:
            question("Error getting the budget")
        stat = 'Your budget for category %s is %d . anything else I can help you' % (category, int(budget))
        pass_parameter(category)
        pass_response(stat)
        return question(stat).reprompt("I didn't get that. Can you say it again?")
    else:
        stat = "I didn't get that. Can you say it again?"
        pass_parameter('none')
        pass_response(stat)
        return question(stat)



@ask.intent("CreditBooster")
def creditScore():
    amountOwed = 0
    dic = web.getBalanceAndLimit(pnc_api_token)
    for key in dic:
        amountOwed += dic[key][0]
    #amountOwed = sum(web.getBalanceAndLimit(pnc_api_token).values())
    creditLimit = amountOwed * 3
    stat = creditTests(amountOwed, creditLimit)
    pass_parameter('none')
    pass_response(stat)
    return statement(stat)


if __name__ == '__main__':
    # initalize pnc_api_token
    s = requests.session()
    s.keep_alive = False
    pnc_api_token = web.login(USERNAME, PASSWORD)
    app.run(debug=True)
