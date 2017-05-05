from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

transaction_type_global = ''

@ask.intent("BudgetAddAmountIntent", mapping={'budget_amount': 'BudgetAmount'})
def setBudget(budget_amount):
    if budget_amount and transaction_type_global:
        # PNC api to create budget
        answer = 'You created a budget with ${} for healthcare successfully. Do you want to \
                    share the budget plan on Twitter?'.format(budget_amount, transaction_type_global)
        repromt_msg = "Sorry, could you please say the budget amount again?"
        transaction_type_global = ''
        return question(answer).reprompt(repromt_msg)
    else if not transaction_type_global:
        # The category is missing!!!
        # I don't konw what to do here





@ask.intent("BudgetCreateIntent", mapping={'transaction_type': 'TransactionCategory'})
def createBudget(transaction_type):
    transaction_type_global = transaction_type
    question_phrase = "People in similar financial situation in your area, I suggest you to set {} dollars for {}. What amount do you want to set?".format(500, transaction_type)
    return question(question_phrase)
