# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import web
from socialMediaHelper import tweet

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

tweet('testing tweet')

# requests.adapters.DEFAULT_RETRIES = 500


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
    #welcome_message = 'Hello there, just a quick reminder. you have a car loan payment of 3000 dollars due this Saturday . . what can I do for you today?'
    welcome_message = 'Hello there.'
    # question expect response
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
    stat = ' '.join(['Your', account_type, 'balance is'])
    return question(' '.join([stat, ' . ', str(bal), ' . ', 'anything else I can help you'])).reprompt("I didn't get that. Can you say it again?")


# js = json.loads('{"version": "1.0", "response": {"outputSpeech": {"type": "PlainText","text": "Your standard checking balance is  .  5000.0  .  anything else I can help you"},"shouldEndSession": false},"sessionAttributes": {}}')

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
    return question(stat).reprompt("I didn't get that. Can you say it again?")



@ask.intent("FAQIntent")
def FAQ():
    pass


@ask.intent("LostCardIntent")
def lost_card_handler():
    answer = 'If your card has been lost or stolen, contact us immediately at one of the following phone numbers. . Personal Debit Cards . 1 888 762 2265 . Virtual Wallet . 1 800 352 2255 . Business Debit Cards . 1 877 287 2654 . PNC Premier Traveler Visa Signature Credit Card . 1 877 588 3602 . PNC Premier Traveler Reserve Visa Signature credit card . 1 877 631 8996'
    stat = ' '.join([answer, ' . ', 'anything else I can help you'])
    return question(stat).reprompt("I didn't get that. Can you say it again?")


@ask.intent("AdviceIntent")
def adviceWealth():
    # get balance from saving account
    bal = 5000

    #interest rate for saving is constant for all balance
    #ref https://apps.pnc.com/rates/servlet/DepositRatesSearch?productGroup=mmarket
    ir = 0.0001

    #interest rate for performance checking in money market
    #ref https://apps.pnc.com/rates/servlet/DepositRatesSearch?productGroup=mmarket
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

    ie = ir*bal
    mmie = mmir*bal

    stat = ' '.join(['You have a healthy portfolio of ', str(bal), 'dollars in saving. You are getting', str(ie), 'interet earnings every year. You can do even greater with money market and your interest earning will be', str(mmie), 'dollars per year. . anything else I can help you'])
    return question(stat).reprompt("I didn't get that. Can you say it again?")




@ask.intent("BudgetIntent", mapping={'budget_amount': 'BudgetAmount', 'transaction_type': 'TransactionCategory'})
def setBudget(budget_amount, transaction_type):
    if budget_amount and transaction_type:
        answer = 'ok. budget for' + transaction_type + 'is set succesfully'
    # elif not transaction_type:
    #     return question('what is the amount')#.prompt()
    stat = ' '.join([answer, ' . ', 'anything else I can help you'])
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
        return question(answer).reprompt(repromt_msg)
    # if not transaction_type_global:
    #     return question('which category you want to add')


@ask.intent("BudgetTriggerIntent")
def triggerBudget():
    # if budget_amount and transaction_type_global:
    #     # PNC api to create budget
    #     answer = 'You created a budget with ${} for healthcare successfully. Do you want to \
    #                 share the budget plan on Twitter?'.format(budget_amount, transaction_type_global)
    #     repromt_msg = "Sorry, could you please say the budget amount again?"
    #     session.attributes['budget_amount'] = budget_amount
    #     session.attributes['transaction_type_global'] = transaction_type_global
    #     transaction_type_global = ''
    #     return question(answer).reprompt(repromt_msg)
    # else if not transaction_type_global:
    return question('which category you want to add the budget')



@ask.intent("BudgetAddCategoryIntent", mapping={'transaction_type': 'TransactionCategory'})
def addCatBudget(transaction_type):
    global transaction_type_global
    transaction_type_global = transaction_type
    question_phrase = "People in similar financial situation in your area, I suggest you to set {} dollars for {}. What amount do you want to set?".format(500, transaction_type)
    return question(question_phrase)


# handle user input yes or no response
# user input is intent
@ask.intent("MyYesIntent")
def twitter_share():
    print 'SHARE'
    budget_amount = session.attributes['budget_amount']
    transaction_type_global = session.attributes['transaction_type_global']
    print 'AMO',budget_amount, 'TYPE',transaction_type_global
    tweet('I have set a ${} budget for {} in my PNC account through out cute Alexa PNC Assistant'.format(budget_amount, transaction_type_global))
    stat = 'You have set a ${} budget for {} in my PNC account through out cute Alexa PNC Assistant . anything else I can help you'.format(budget_amount, transaction_type_global)
    return question(stat)


@ask.intent("MyNoIntent")
def no_intent():
    stat = 'okay. what else can i do for you'
    return question(stat)


if __name__ == '__main__':
    # initalize pnc_api_token
    s = requests.session()
    s.keep_alive = False
    pnc_api_token = web.login(USERNAME, PASSWORD)
    app.run(debug=True)
