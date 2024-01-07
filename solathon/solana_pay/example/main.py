from typing import Any, List, Literal
from keypair import Keypair
from solana_pay import encode_url, create_qr, find_reference, validate_transfer
from client import Client
from constants import MERCHENT_WALLET
from example.simulate_wallet_interaction import simulate_wallet_interaction

def simulate_checkout_params() -> List[Any]:
    label = "Jungle Cats store"
    message = "Jungle Cats store - your order - #001234"
    memo = "JC#4098"
    amount = 0.000000001
    reference = Keypair().public_key

    return [label, message, amount, memo, reference]

def main():
    # Tracking payment status through out the process
    payment_status: Literal["pending", "confirmed", "validated"] = None

    print("⚡Connect to cluster")
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
    [label, message, amount, memo, reference] = simulate_checkout_params()

    '''
    * Create a payment request link
    *
    * Solana Pay uses a standard URL scheme across wallets for native SOL and SPL Token payments.
    * Several parameters are encoded within the link representing an intent to collect payment from a customer.
    '''
    print("🔗 Generate a link for the transfer")
    url = encode_url({"recipient": MERCHENT_WALLET, "label": label, "message": message,
                    "memo": memo, "amount": amount, "reference": reference})

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
    validate_transfer(client, sign.signature, { "recipient": MERCHENT_WALLET, "amount": amount, "memo": memo, "references": [reference] })

    payment_status = "validated"
    print("🎉 Payment is validated")
    print("📦 Order can be shipped to customer")

if __name__ == "__main__":
    main()