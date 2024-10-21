import json
from web3 import Web3
from eth_account import Account
from django.conf import settings

# Connect to the Sepolia Testnet (or your PoA network provider URL)
web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))

# Load the ABI and contract address
with open('core/abi/healthcare_contract_abi.json') as f:
    contract_abi = json.load(f)

contract_address = '0x01641268E37C8321A021f3E5cc6f005EBeB4b4d7'

# Create a contract instance
healthcare_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to add patient data
def add_patient_data(patient_name, diagnosis, treatment):
    private_key = '2182c82942eb17fe568eac16cc5e9d676ca505487c6d2006784799766cef283b'
    account = Account.from_key(private_key)

    # Build and send the transaction using transact()
    transaction = healthcare_contract.functions.addRecord(patient_name, diagnosis, treatment).transact({
        'from': account.address,
        'chainId': 11155111,  # Sepolia Testnet Chain ID
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(account.address),
    })

    return transaction.hex()


