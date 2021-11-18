This is the invoice generator script to run on windows local machine

It generates 10 invoices every 3 hours to the custumers defined on the 
custumer.xlsx file, and ends after 24 hours of operation.

Steps:
1) Install dependencies on requirements.txt:
	- $ pip install -r requirements.txt

2) Generate private and public keys and store them on /file/keys:
	- name private key: "private-key.pem"
	- name public key : "public-key.pem"

3) Run main.py:
