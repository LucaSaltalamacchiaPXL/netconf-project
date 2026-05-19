from ncclient import manager
import requests
import sys

ROUTER = "10.0.2.15"
PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"

GITHUB_URL = "https://raw.githubusercontent.com/LucaSaltalamacchiaPXL/netconf-project/main/config.xml"

def get_config():
    try:
        print("Downloading config from GitHub...")
        response = requests.get(GITHUB_URL, headers={"Cache-Control": "no-cache"}, timeout=20)
        response.raise_for_status()
        config = response.text.strip()
        print("\n--- CONFIG FROM GITHUB ---")
        print(config)
        print("--- END CONFIG ---\n")
        return config
    except Exception as e:
        print("ERROR downloading config:", e)
        sys.exit(1)

def main():
    config_xml = get_config()

    payload = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
{config_xml}
</config>
"""

    try:
        print("Connecting to router...")

        with manager.connect(
            host=ROUTER,
            port=PORT,
            username=USERNAME,
            password=PASSWORD,
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False,
            timeout=30
        ) as m:

            print("Connected")
            print("Sending config to running datastore...")

            reply = m.edit_config(
                target="running",
                config=payload,
                default_operation="merge"
            )

            print(reply.xml)
            print("DEPLOYMENT SUCCESSFUL")

    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
