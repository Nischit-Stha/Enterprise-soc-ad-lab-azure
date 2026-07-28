"""
Wazuh Agent Summary Script
----------------------------
Authenticates to the Wazuh Manager API and prints a summary of
enrolled agents (name, status, IP address).

Credentials are read from environment variables, not hardcoded:
    export WAZUH_API_USER="your_username"
    export WAZUH_API_PASS="your_password"
"""

import requests
import urllib3
import os
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Config ---
WAZUH_API = "https://localhost:55000"
USERNAME = os.getenv("WAZUH_API_USER", "your_username_here")
PASSWORD = os.getenv("WAZUH_API_PASS", "your_password_here")


def get_token():
    resp = requests.post(
        f"{WAZUH_API}/security/user/authenticate",
        auth=(USERNAME, PASSWORD),
        verify=False
    )
    resp.raise_for_status()
    return resp.json()["data"]["token"]


def get_agents(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{WAZUH_API}/agents", headers=headers, verify=False)
    resp.raise_for_status()
    return resp.json()["data"]["affected_items"]


def main():
    print(f"=== Wazuh Agent Summary — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    token = get_token()
    agents = get_agents(token)

    for agent in agents:
        name = agent.get("name", "unknown")
        status = agent.get("status", "unknown")
        ip = agent.get("ip", "n/a")
        print(f"Agent: {name:15} | Status: {status:12} | IP: {ip}")


if __name__ == "__main__":
    main()

