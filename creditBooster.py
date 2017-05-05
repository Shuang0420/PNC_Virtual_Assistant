#! /bin/python

import numpy
def creditTest1(credit_balance, credit_limit):
	"""
	Credit usage: soft line 30%, hard line 80%
	"""
	if credit_balance < 0.3*credit_limit:
		return "passed"
	elif credit_balance< 0.8*credit_limit:
		soft_line = 0.3*credit_limit
		clear = credit_balance - soft_line
		return " ".join(["Your credit score will boost if the credit payment outstanding is constantly under", str(soft_line), "dollars. Currently you are using", str(credit_balance), "dollars. Your credit score will be even better when you pay at least", str(clear), "dollars today?"])
	else:
		hard_line = 0.8*credit_limit
		clear = credit_balance - hard_line
		return " ".join(["Warning. You have exceeded", str(hard_line), "credit threshold and it will largely impact on the credit score. Your credit score will increase when you pay at least", str(clear), "dollars."])


def creditTest2():
	"""
	payment history: regularly pay on time? Any credit history?
	"""
	return "pass"

def creditTest3():
	"""
	age of credit: average credit history
	"""
	return "pass"

def creditTest4():
	"""
	no. of accounts from credit card, card loan, home loan
	"""
	return "pass"

def creditTest5():
	"""
	hard pull
	"""
	return "pass"

def creditTests(credit_balance, credit_limit):
	"""
	run all the credit payment test
	"""
	results = [creditTest1(credit_balance, credit_limit), creditTest2(), creditTest3(), creditTest4(), creditTest5() ]
	passed = sum(numpy.array(results) == 'pass')
	abnormal = " ".join([i for i in results if i!= "pass"])
	stat = " ".join(["Check completed. You are doing a great job in passing", str(passed), "out of 5 credit payment tests.", str(abnormal)])
	return stat

print creditTests(2000,6000)
