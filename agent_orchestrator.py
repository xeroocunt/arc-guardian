import os
import time
import json
import secrets
import sys
import io
from web3 import Web3
from eth_account import Account

# Force UTF-8 encoding for stdout to handle emojis on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
RPC_URL = os.getenv("ARC_RPC_URL", "https://rpc.testnet.arc.network")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_PATH = "contracts/ArcGreeting.sol"
CHAIN_ID = 5042002  # Arc Testnet

def setup_agent():
    print("-----------------------------------------")
    print("🤖 ARC AI AGENT ORCHESTRATOR INITIALIZING")
    print("-----------------------------------------")
    
    # 1. Connect to Arc with timeout and retries
    print(f"🔗 Attempting to connect to: {RPC_URL}")
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'timeout': 30}))
    
    connected = False
    for attempt in range(3):
        if w3.is_connected():
            connected = True
            break
        print(f"⚠️ Connection attempt {attempt + 1} failed. Retrying...")
        time.sleep(2)

    if not connected:
        print("❌ Error: Could not connect to Arc Network after multiple attempts.")
        return None, None
    print(f"✅ Connected to Arc Testnet (Block: {w3.eth.block_number})")

    # 2. Setup Wallet
    if not PRIVATE_KEY:
        print("📍 No Private Key found in .env. Generating a temporary test wallet...")
        priv = secrets.token_hex(32)
        acct = Account.from_key("0x" + priv)
        print(f"🔹 Temp Wallet: {acct.address}")
        print("💡 NOTE: You need to fund this address with testnet USDC to deploy.")
        return w3, acct
    else:
        acct = Account.from_key(PRIVATE_KEY)
        print(f"📍 Using Wallet: {acct.address}")
    
    return w3, acct

def compile_contract():
    print("\n🛠️ Compiling Smart Contract...")
    install_solc("0.8.20")
    
    with open(CONTRACT_PATH, "r") as file:
        source_code = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {CONTRACT_PATH: {"content": source_code}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.20",
    )

    bytecode = compiled_sol["contracts"][CONTRACT_PATH]["ArcGreeting"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_sol["contracts"][CONTRACT_PATH]["ArcGreeting"]["metadata"])["output"]["abi"]
    
    return abi, bytecode

def deploy_contract(w3, acct, abi, bytecode):
    print("\n🚀 Deploying Contract to Arc Network...")
    
    ArcGreeting = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Get nonce
    nonce = w3.eth.get_transaction_count(acct.address)
    
    # Build transaction
    transaction = ArcGreeting.constructor("Initial Greeting from AI Agent").build_transaction({
        "chainId": CHAIN_ID,
        "gasPrice": w3.eth.gas_price,
        "from": acct.address,
        "nonce": nonce,
    })
    
    # Sign and send
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=acct.key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    print(f"⏳ Transaction Sent! Hash: {tx_hash.hex()}")
    print("⏳ Waiting for confirmation...")
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print(f"✅ Contract Deployed! Address: {contract_address}")
    
    # Automatically update .env file
    update_env_file("CONTRACT_ADDRESS", contract_address)
    
    return contract_address

def update_env_file(key, value):
    env_path = ".env"
    lines = []
    found = False
    
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
            
    if not found:
        lines.append(f"{key}={value}\n")
        
    with open(env_path, "w") as f:
        f.writelines(lines)
    print(f"📝 Updated {env_path} with {key}={value}")

def autonomous_loop(w3, acct, contract_address, abi):
    print("\n🧠 Agent entering autonomous loop...")
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    states = [
        "Analyzing Arc network liquidity...",
        "Optimizing cross-chain stablecoin pathways...",
        "Scanning for enterprise-grade opportunities...",
        "Hardening economic operating system...",
        "Calibrating neural transaction parameters...",
        "Monitoring Arc Testnet block production...",
        "System check: All subsystems operational.",
        "Executing autonomous treasury rebalancing..."
    ]
    
    i = 0
    while True:
        try:
            status = states[i % len(states)]
            print(f"\n🤖 Agent Decision: Setting status to '{status}'")
            
            nonce = w3.eth.get_transaction_count(acct.address)
            txn = contract.functions.setGreeting(status).build_transaction({
                "chainId": CHAIN_ID,
                "gasPrice": w3.eth.gas_price,
                "from": acct.address,
                "nonce": nonce,
            })
            
            signed_txn = w3.eth.account.sign_transaction(txn, private_key=acct.key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"✅ On-chain Update Sent: {tx_hash.hex()}")
            
            i += 1
            print("⏳ Sleeping for 60 seconds...")
            time.sleep(60)
            
        except Exception as e:
            print(f"❌ Error in loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    try:
        w3, acct = setup_agent()
        if w3 and acct:
            # Check for funds before proceeding
            print(f"💰 Checking balance for {acct.address}...")
            while True:
                balance = w3.eth.get_balance(acct.address)
                if balance > 0:
                    print(f"💵 Balance detected: {w3.from_wei(balance, 'ether')} USDC")
                    break
                print("⏳ Waiting for funds... Please visit https://faucet.circle.com and fund your wallet.")
                print(f"📍 Address: {acct.address}")
                time.sleep(10)

            abi, bytecode = compile_contract()
            
            # Check if we should deploy or use existing
            contract_addr = os.getenv("CONTRACT_ADDRESS")
            if not contract_addr or contract_addr == "0x":
                contract_addr = deploy_contract(w3, acct, abi, bytecode)
            else:
                print(f"🔗 Using existing contract at: {contract_addr}")
            
            print("\n-----------------------------------------")
            print("🌟 DASHBOARD READY")
            print(f"🔗 Click here: http://localhost:8000/dashboard.html?addr={contract_addr}")
            print("-----------------------------------------\n")
            
            autonomous_loop(w3, acct, contract_addr, abi)
    except KeyboardInterrupt:
        print("\n👋 Orchestrator shutdown by user.")
    except Exception as e:
        print(f"💥 Critical Error: {e}")
