from web3 import Web3
import time
import random
import requests

# Connect to the Monad network via Infura RPC
infura_url = "https://testnet-rpc.monad.xyz"
web3 = Web3(Web3.HTTPProvider(infura_url, request_kwargs={'timeout': 60}))

# Check if the connection is successful
if not web3.is_connected():
    raise Exception("Failed to connect to Optimism network")

# Constants
CHAIN_ID = 10143  # Optimism Chain ID
MAX_RETRIES = 3  # Maximum retries per transaction

# Function to generate a random contract address
def generate_random_contract_address():
    return Web3.to_checksum_address("0x" + "".join(random.choices("0123456789abcdef", k=40)))

# Function to generate a random wallet address
def generate_random_wallet_address():
    random_address = "0x" + "".join(random.choices("0123456789abcdef", k=40))
    return Web3.to_checksum_address(random_address)

# Note: The function to generate human-readable random contract details has been removed.

# Function to send ETH transaction to a randomly generated contract address
def send_eth_to_contract(private_key, repetitions, amount):
    sender_address = web3.eth.account.from_key(private_key).address
    value_to_send = web3.to_wei(amount, 'ether')

    for i in range(repetitions):
        to_address = generate_random_contract_address()
        # Removed the generation and printing of contract details

        for attempt in range(MAX_RETRIES):
            try:
                nonce = web3.eth.get_transaction_count(sender_address)
                gas_price = web3.eth.gas_price * 1.1
                estimated_gas_limit = web3.eth.estimate_gas({
                    'from': sender_address,
                    'to': to_address,
                    'value': value_to_send
                })
                gas_limit = int(estimated_gas_limit * 1.2)

                tx = {
                    'nonce': nonce,
                    'to': to_address,
                    'value': value_to_send,
                    'gas': gas_limit,
                    'gasPrice': int(gas_price),
                    'chainId': CHAIN_ID
                }

                signed_tx = web3.eth.account.sign_transaction(tx, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                print(f"Transaction {i+1}/{repetitions} sent to {to_address} with {amount} ETH! Tx Hash: {web3.to_hex(tx_hash)}")
                break
            except requests.exceptions.HTTPError as e:
                print(f"HTTPError on attempt {attempt+1}: {e}")
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(5)
                else:
                    print("Transaction failed after maximum retries.")

        time.sleep(5)

    print("Task done! Now go say Thank You to Petrate")

# Main script
if __name__ == "__main__":
    private_key = input("Enter your private key: ")
    repetitions = int(input("How many times do you want to perform the transaction? "))
    choice = input("Do you want to send 0 ETH to contracts (1), 0.00001 ETH to wallets (2), or send a custom ETH amount to contracts (3)? Enter 1, 2, or 3: ")
    
    if choice == "1":
        send_eth_to_contract(private_key, repetitions, 0)
    elif choice == "2":
        send_eth_to_contract(private_key, repetitions, 0.00001)
    elif choice == "3":
        amount = float(input("Enter the amount of ETH to send: "))
        send_eth_to_contract(private_key, repetitions, amount)
    else:
        print("Invalid choice. Exiting.")

