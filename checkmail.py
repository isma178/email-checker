#!/usr/bin/env python3
import os
import argparse
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)

def gmail_session():
	global result
	sess_url = "https://accounts.google.com/signup/v2/webcreateaccount?service=mail&flowEntry=SignUp"
	response = requests.get(sess_url, timeout=3, stream=False, verify=False)
	soup = BeautifulSoup(response.content, "html.parser")
	parse=soup.find_all("div", {"class": "JhUD8d SQNfcc vLGJgb"})[0].get("data-initial-setup-data")
	result=parse.split(",")[13]

def gmail_check():
	global status
	headers['Google-Accounts-Xsrf'] = "1"
	headers["Content-Type"] = "application/x-www-form-urlencoded"
	check_url = "https://accounts.google.com/_/signup/webusernameavailability"
	payload = "f.req=[" + result + ',"","","' + email + '"]'
	req = requests.post(check_url, data=payload, timeout=3, stream=False, verify=False, headers=headers)
	status = req.content
	# Temporary fix
	status = status.decode()
	check_status = status.split(",")[1]
	resp_dict = {"1": "[+] Email is available!  ", "2": "[-] Email is already use!", "3": "[-] Email is not allowed!"}
	status = resp_dict.get(check_status)
	print(u"{0:34} Domain: {1:10}".format(status,"gmail.com"))
	# Fixed?
	if check_status == "1":
		email_list.append(email + "@gmail.com")

parser = argparse.ArgumentParser(description="Example: %(prog)s --email username", usage="%(prog)s --email username")
parser.add_argument("-e", "--email", help="Username for check email available on yandex, mail, gmail, rambler, yahoo")
args = parser.parse_args()
email = args.email

os.system("clear")

headers = {"UserAgent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"}
email_list = []

print("-------------------------------------------------")
print("         EXISTENCE EMAIL CHECKER (by p0z)        ")
print("-------------------------------------------------")

if email is None:
	print("Run script option -h")
	os._exit(0)

print("Check email: ", email)

print("--------------------GMAIL.COM--------------------")
gmail_session()
gmail_check()
print("-------------------------------------------------")

print("All emails:")
print(email_list)
