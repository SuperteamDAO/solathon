from create_transfer import create_transfer
from parse_url import parse_url
from client import Client
from example.constants import CUSTOMER_WALLET


def simulate_wallet_interaction(client: Client, url: str) -> None:
    print("🔗 Decode the url and get transfer parameters")
    decoded = parse_url(url)

    print("🔑 Create a transfer and simulate sending it")
    new_transfer = create_transfer(client, CUSTOMER_WALLET, {
        "recipient": decoded.recipient, "amount": decoded.amount, "memo": decoded.memo, "references": decoded.reference})

    client.send_transaction(new_transfer)
