import sys
import subprocess
import os

def run_automation():
    print("==================================================")
    print("ARC AGENT SYSTEM: AUTOMATIC SETUP & LAUNCH")
    print("==================================================")
    
    # 1. Install dependencies
    print("\nStep 1: Installing required Python libraries...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'web3', 'eth-account', 'py-solc-x', 'python-dotenv'])
        print("Installation successful.")
    except Exception as e:
        print(f"Error installing libraries: {e}")
        return

    # 2. Check for .env file
    if not os.path.exists(".env"):
        print("\nStep 2: Creating a template .env file...")
        with open(".env", "w") as f:
            f.write("ARC_RPC_URL=https://rpc.testnet.arc.network\n")
            f.write("PRIVATE_KEY=\n")
            f.write("CONTRACT_ADDRESS=\n")
        print(".env created. (Please add your PRIVATE_KEY if you have one!)")

    # 3. Start Dashboard Server
    print("\nStep 3: Starting Dashboard server on http://localhost:8000...")
    try:
        # Start server in background
        subprocess.Popen([sys.executable, '-m', 'http.server', '8000'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Dashboard live at http://localhost:8000/dashboard.html")
    except Exception as e:
        print(f"Could not start dashboard server: {e}")

    # 4. Launch the agent
    print("\nStep 4: Launching Arc AI Agent Orchestrator...")
    print("--------------------------------------------------")
    
    try:
        # We run the actual agent script
        subprocess.call([sys.executable, 'agent_orchestrator.py'])
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")
    except Exception as e:
        print(f"Error launching agent: {e}")

if __name__ == "__main__":
    run_automation()
