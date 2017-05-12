# PNC_Virtual_Assistant
Quick Tutorial [Alexa 开发新技能](http://www.shuang0420.com/2017/05/02/Alexa%20开发新技能/)

## Requirements
- flask == 0.12.1
- flask_ask == 0.9.3
- unidecode == 0.4.20
- unirest == 1.1.7

## Usage
Connect with your Alexa and have following conversation.


### Balance/Transaction checking
User: Alexa, start PNC assistant.
Alexa: Hello there, just a quick reminder. You have a car loan payment of 3000 dollars due this Saturday. What can I do for you today?

User: Alexa, what is my balance/(What is my balance of savings(/{ACCOUNT TYPE}) account?)
Alexa: Your standard checking account balance is {NUMBER} dollars. Anything else I can help you?

User: Alexa, how much I spend on Fast Food today(/last week/last month/last year)?
Alexa: You spent {NUMBER} dollars today(/last week/last month/last year). Anything else I can help you?

### Q&A
User: Alexa, I lost my card, what should I do?
Alexa: If your card has been lost or stolen, contact us immediately at one of the following phone numbers.
Personal Debit Cards 1-888-PNC-BANK (1-888-762-2265)


### Personal Financial Expert
#### Add a budget plan:
User: Alexa, I want to set a new budget?
Alexa: Which category you want to add the budget?

User: Healthcare category
Alexa: Actually, according to people in similar financial situation in pittsburgh, I suggest you to set 500 dollars for {CATEGORY}. What amount do you want to set?

User: $300 dollars
Alexa: Thank you. You created a budget with $300 for Healthcare successfully. Do you want to share the budget plan with your family or friends through Twitter?

User: Ok please tweet.
Alexa: You have set a ${NUMBER} dollars budget for {CATEGORY} in your PNC account through cute Alexa PNC Assistant. Anything else I can help you?


#### Check budget
User: Please tell me my budget for book(/{CATEGORY})?
Alexa: Your budget for {CATEGORY} is {NUMBER} dollars. Anything else I can help you?


#### Ask for Wealth Management Advice
User: Alexa, how to invest my money?
Alexa: You have a healthy portfolio of {NUMBER} dollars in saving. You are getting {NUMBER} interest earnings every year. You can do even greater with money market and your interest earning will be {NUMBER} dollars per year. Anything else I can help you?


### Credit Score Boosting
User: Alexa, how can I boost my credit score?
Alexa: Check completed. You are doing a great job in passing {NUMBER} out of 5 credit payment tests.



## Reference Link
[Slot Type Reference](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/built-in-intent-ref/slot-type-reference)
