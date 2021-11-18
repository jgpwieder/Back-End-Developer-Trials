This script runs on windows

It listens to invoices on Stark Bank account, if an invoice is credited to the account
it transfers the amount received minus fees to Stark Bank.
Steps:
1) Install dependencies on requirements.txt:
	- Run: "$ pip install -r requirements.txt"

2) Generate private and public keys and store them on /file/keys:
	- name private key: "private-key.pem"
	- name public key : "public-key.pem"

3) Run ngrok:
	- Run: "$ ngrok http 5000"

4) Create a webhook endpoint on Stark Bank using the https url provided by ngrok public server.

5) Run main.py
	