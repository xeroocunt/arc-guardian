from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = "https://rpc.testnet.arc.network"
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ABI = ["function getGreeting() view returns (string)"]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

try:
    greeting = contract.functions.getGreeting().call()
    print(f"Current Greeting: {greeting}")
except Exception as e:
    print(f"Error: {e}")
