import starkbank
from datetime import datetime, timedelta
import pandas as pd
from random import randrange
import schedule
import time

# Store the initial time:
initial_time = time.time()

# Read and store customers information for invoices:
customers = pd.read_excel('Customers.xlsx')

# Read the keys from .pem file:
file_public = open('file\\keys\\public-key.pem', mode='r')
file_private = open('file\\keys\\private-key.pem', mode='r')

# Store the keys
key_public = file_public.read()
key_private = file_private.read()

# Close file with the keys:
file_public.close()
file_private.close()

# Create project object:
project = starkbank.Project(
    environment="sandbox",
    id="5333073948311552",
    private_key=key_private)

# Set default user and inform StarkBank:
starkbank.user = project


# Define function to create invoices based on data from excel sheet
def invoice_function():
    # Define for loop, range = number of invoices every 3 hours
    for i in range(10):
        # Choose a random client from the excel sheet
        index = randrange(0, 20)
        # Create invoices:
        invoices = starkbank.invoice.create([
            starkbank.Invoice(
                amount=int(customers.iloc[index, 0])*100,
                name=customers.iloc[index, 1],
                tax_id=customers.iloc[index, 2],
                due=datetime.utcnow() + timedelta(hours=1),
                expiration=timedelta(hours=3).total_seconds(),
                fine=5,  # 5%
                interest=2.5,  # 2.5% per month
                tags=["immediate"]
            )])
        # Print invoices:
        for invoice in invoices:
            print(invoice)


# Schedule will wait 3 hours before running invoice function, so run one first:
invoice_function()

# Schedule to run the invoice function every 3 hours
schedule.every(3).hours.do(invoice_function)
while True:
    schedule.run_pending()
    # Set the refresh rate to 1/100*scheduled time = 0.03 hours =~ 2min, 1% error
    time.sleep(120)
    # Break the loop if 24 hours have passed since the initial time:
    if time.time() > initial_time+24*60*60:
        break
