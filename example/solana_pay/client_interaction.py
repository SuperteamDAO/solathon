from solathon import Client
from solathon.solana_pay import create_transfer, parse_url

CUSTOMER_WALLET = Keypair.from_private_key([
    169, 48, 146, 127, 191, 185, 98, 158, 130, 159, 205, 137, 2, 146, 85, 1, 93, 107, 98, 90, 245, 69, 40, 39, 220,
    78, 226, 249, 231, 254, 92, 13, 186, 138, 174, 147, 156, 143, 248, 132, 28, 206, 134, 228, 241, 192, 94, 44,
    177, 15, 41, 219, 124, 116, 255, 78, 172, 209, 106, 78, 37, 169, 115, 146,
]) # This should be funded with some SOL

def simulate_wallet_interaction(client: Client, url: str) -> None:
    print("🔗 Decode the url and get transfer parameters")
    decoded = parse_url(url)

    print("🔑 Create a transfer and simulate sending it")
    new_transfer = create_transfer(client, CUSTOMER_WALLET, {
        "recipient": decoded.recipient, "amount": decoded.amount, "memo": decoded.memo, "references": decoded.reference})

    client.send_transaction(new_transfer)
