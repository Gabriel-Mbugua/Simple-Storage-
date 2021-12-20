import json
import os
from web3 import Web3
from solcx import compile_standard
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


#  Compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            },
        },
    },
    solc_version="0.6.0",
)

# return output into file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


#  connecting to rinkeby testnet
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/a934f16b89c143b0805bd8965dc6219a")
)
chain_id = 4
my_address = "0x9031e7b28B90cC37aDD7Ef914b1d5132FB0d51DF"
# always add '0x' to the front of a private key in python
private_key = os.getenv("PRIVATE_KEY")

# Creat the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# 2: Sign a transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction,
    private_key=private_key,
)

# 3: Send a transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
# wait for transaction has to go through
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")


# Working with the contract requires:
# Contract address
# Contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value (no state change).
# Transact -> Makes state change.

# Initial value of fav number
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash=send_store_txn)
print("Updated!")
print(simple_storage.functions.retrieve().call())
