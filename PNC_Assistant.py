from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode


# username and password for reddit
USERNAME = 'shuang'
PASSWORD = '0420'


# define Flask app
app = Flask(__name__)
# give basic endpoint, can be flask skill/program endpoint
ask = Ask(app, "/reddit_reader")

# check balance
def getBalance():
    pass



# track transaction
def checkTransaction():
    pass




# get answer to frequent asked questions
def getFAQ():
    pass



# set home url path
@app.route('/')
def homepage():
    return 'hi there, how ya doin?'


@ask.launch
def start_skill():
    # it will say
    welcome_message = 'Hello there, would you like the news?'
    # question expect response
    return question(welcome_message)


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



if __name__ == '__main__':
    app.run(debug=True)
