import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

RPC_URL = "https://rpc.testnet.arc.network"
ADDRESS = "0x74E4b1d2590688Aa3363D13f4537678a98a3FF22"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if w3.is_connected():
    balance = w3.eth.get_balance(ADDRESS)
    print(f"Native Balance: {w3.from_wei(balance, 'ether')} ARC/USDC")
else:
    print("Failed to connect")
