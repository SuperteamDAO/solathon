import time
from typing import Any, List, Literal
from solathon.solana_pay import encode_url, create_qr, find_reference, validate_transfer
from solathon import Client, Keypair, PublicKey
from client_interaction import simulate_wallet_interaction

MERCHENT_WALLET = PublicKey("mvines9iiHiQTysrwkJjGf2gb9Ex9jXJX8ns3qwf2kN")

CUSTOMER_WALLET = Keypair.from_private_key([
    169, 48, 146, 127, 191, 185, 98, 158, 130, 159, 205, 137, 2, 146, 85, 1, 93, 107, 98, 90, 245, 69, 40, 39, 220,
    78, 226, 249, 231, 254, 92, 13, 186, 138, 174, 147, 156, 143, 248, 132, 28, 206, 134, 228, 241, 192, 94, 44,
    177, 15, 41, 219, 124, 116, 255, 78, 172, 209, 106, 78, 37, 169, 115, 146,
]) # This should be funded with some SOL


def checkout_params() -> List[Any]:
    label = "Jungle Cats store"
    message = "Jungle Cats store - your order - #001234"
    amount = 0.01
    reference = Keypair().public_key

    return [label, message, amount, reference]

def main():
    # Tracking payment status through out the process
    payment_status: Literal["pending", "confirmed", "validated"] = None

    print("⚡ Connect to cluster")
    client = Client("https://api.devnet.solana.com")

    '''
    * Simulate a checkout experience
    *
    * Recommendation:
    * `amount` and `reference` should be created in a trusted environment (server).
    * The `reference` should be unique to a single customer session,
    * and will be used to find and validate the payment in the future.
    '''
    print("⭐ Simulate a checkout and get transaction parameters")
    [label, message, amount, reference] = checkout_params()

    '''
    * Create a payment request link
    *
    * Solana Pay uses a standard URL scheme across wallets for native SOL and SPL Token payments.
    * Several parameters are encoded within the link representing an intent to collect payment from a customer.
    '''
    print("🔗 Generate a link for the transfer")
    url = encode_url({"recipient": MERCHENT_WALLET, "label": label, "message": message,
                    "amount": amount, "reference": reference})

    print("🤖 Generate a cutomized solana pay QR code for link")
    qr_image_stream = create_qr(url)

    '''
    * Simulate wallet interaction
    *
    * This is only for example purposes. This interaction will be handled by a wallet provider
    '''
    print(
        f"💲Use the generated url({url}) or QR Code on client side for user to send and confirm the transaction")
    simulate_wallet_interaction(client, url)
    
    payment_status = "pending"

    print("⏳ Waiting for payment to be confirmed")
    time.sleep(15)
    
    '''
    * Wait for payment to be confirmed
    *
    * When a customer approves the payment request in their wallet, this transaction exists on-chain.
    * You can use any references encoded into the payment link to find the exact transaction on-chain.
    * Important to note that we can only find the transaction when it's **confirmed**
    '''
    print("🔍 Find the transaction signature from reference public key")
    sign = find_reference(client, reference)

    payment_status = "confirmed"

    '''
    * Validate transaction
    *
    * Once the `findTransactionSignature` function returns a signature,
    * it confirms that a transaction with reference to this order has been recorded on-chain.
    *
    * `validateTransactionSignature` allows you to validate that the transaction signature
    * found matches the transaction that you expected.
    '''
    print("🔑 Validate the transaction")
    validate_transfer(client, sign.signature, { "recipient": MERCHENT_WALLET, "amount": amount, "reference": [reference] })

    payment_status = "validated"
    print("🎉 Payment is validated")
    print("📦 Order can be shipped to customer")

if __name__ == "__main__":
    main()