from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv('RPC_URL')))

SAFE_TOKEN = Web3.to_checksum_address('0x5aFE3855358E112B5647B952709E6165e1c1eEEe')
FACTORY = Web3.to_checksum_address('0xB93427b83573C8F27a08A909045c3e809610411a')

# Load all ABIs 
with open('abi/safe_token.json') as f:
    safe_abi = json.load(f)
    
with open('abi/llama_contract.json') as f:
    vest_abi = json.load(f)

with open('abi/llama_factory.json') as f:
    factory_abi = json.load(f)

# Load amount from env and convert to wei
amount = int(os.getenv('TOKEN_AMOUNT'))*10**18

# Create Safe Token Approval to Llama Factory, just the call data and print to screen
safe_contract = w3.eth.contract(address=SAFE_TOKEN, abi=safe_abi)
factory_contract = w3.eth.contract(address=FACTORY, abi=factory_abi)
data = safe_contract.functions.approve(factory_contract.address, amount).build_transaction({'from': "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"})['data']
print('Safe Token Approval to Llama Factory')
print(data)

# Create Llama Vesting Contract Creation, just the call data and print to screen
recipient = Web3.to_checksum_address(os.getenv('VESTING_BENEFICIARY'))

vesting_duration = 31536000 # 1 year
cliff = 0 # None
vesting_start= 1713427754
now = w3.eth.get_block('latest').timestamp

print(f'\nSafe Token: {SAFE_TOKEN}\nRecipient: {recipient}\nAmount: {amount}\nDuration: {vesting_duration}\nStart: {now}\nCliff: {cliff}')

