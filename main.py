from flask import Flask, request, abort
import starkbank
from datetime import datetime

# Read the keys from .pem file:
file_public = open('file\\keys\\public-key.pem', mode='r')
file_private = open('file\\keys\\private-key.pem', mode='r')

# Store the keys
key_public = file_public.read()
key_private = file_private.read()

# Create project object:
project = starkbank.Project(
    environment="sandbox",
    id="5333073948311552",
    private_key=key_private)

# Set default user and inform StarkBank:
starkbank.user = project

# Start Flask app:
app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    # Check for POST requests:
    if request.method == 'POST':
        response = request

        # Parse data:
        event = starkbank.event.parse(
            content=response.data.decode("utf-8"),
            signature=response.headers["Digital-Signature"],
        )

        # Get date and time to create a unique external id:
        external_id = datetime.now()

        # Print the information in the invoice:
        print(f'Invoice type: {event.log.type}')
        print(f'Invoice name: {event.log.invoice.name}')
        print(f'Invoice nominal amount: {event.log.invoice.amount}')

        # Transfer amount = nominal amount -fees -discount +fine +interest
        amount_transfer = event.log.invoice.amount-event.log.invoice.fee+event.log.invoice.fine_amount - \
            event.log.invoice.discount_amount+event.log.invoice.interest_amount

        # Transfer the calculated amount to the StarkBank account only if invoice is credited:
        if event.log.type == "credited":
            transfers = starkbank.transfer.create([
                starkbank.Transfer(
                    amount=amount_transfer,
                    bank_code="20018183",
                    branch_code="0001",
                    account_number="6341320293482496",
                    tax_id="20.018.183/0001-80",
                    name="Stark Bank S.A.",
                    tags=["iron", "suit"],
                    external_id=external_id.strftime("%m.%d.%Y.%H.%M.%S.%f")
                )])
            # Print transfer:
            for transfer in transfers:
                print(transfer)

        return 'success', 200
    else:
        abort(400)


# Run app:
if __name__ == "__main__":
    app.run()
