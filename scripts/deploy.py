from ncclient import manager
from ncclient.operations import RPCError
from xml.dom import minidom
import requests
import sys
from datetime import datetime

ROUTER = "10.0.2.15"  # Straks aanpassen naar IP van de fysieke router
PORT = 830
USERNAME = "cisco"
PASSWORD = "cisco123!"

GITHUB_URL = "https://raw.githubusercontent.com/LucaSaltalamacchiaPXL/netconf-project/main/config.xml"


def pretty_xml(xml_data):
    try:
        return minidom.parseString(xml_data).toprettyxml(indent="  ")
    except Exception:
        return xml_data


def get_config_from_github():
    print("[1] Downloading config.xml from GitHub...")
    try:
        response = requests.get(
            GITHUB_URL,
            headers={"Cache-Control": "no-cache"},
            timeout=20
        )

        print(f"HTTP status code: {response.status_code}")

        response.raise_for_status()
        config = response.text.strip()

        if not config:
            print("ERROR: config.xml is empty.")
            sys.exit(1)

        print("\n--- CONFIG FROM GITHUB ---")
        print(config)
        print("--- END CONFIG ---\n")

        return config

    except requests.exceptions.RequestException as e:
        print("ERROR downloading config from GitHub:")
        print(e)
        sys.exit(1)


def build_payload(config_xml):
    return f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
{config_xml}
</config>
"""


def get_running_config(m, title):
    print(f"\n[{title}] Retrieving running configuration...")

    netconf_filter = """
    <filter>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname/>
      </native>
    </filter>
    """

    reply = m.get_config(source="running", filter=netconf_filter)

    print("\n--- RUNNING CONFIG OUTPUT ---")
    print(pretty_xml(reply.xml))
    print("--- END RUNNING CONFIG OUTPUT ---\n")


def deploy_config(payload):
    try:
        print("[2] Connecting to IOS-XE router with NETCONF...")
        print(f"Router: {ROUTER}:{PORT}")
        print(f"Username: {USERNAME}")

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

            print("[OK] NETCONF session established")
            print(f"Session ID: {m.session_id}")

            print("\n[3] Important NETCONF capabilities:")
            for capability in m.server_capabilities:
                cap = str(capability)
                if "base:1." in cap or "Cisco-IOS-XE-native" in cap or "candidate" in cap:
                    print(" -", cap)

            get_running_config(m, "4 BEFORE DEPLOYMENT")

            print("[5] Sending configuration to running datastore...")

            reply = m.edit_config(
                target="running",
                config=payload,
                default_operation="merge"
            )

            print("\n--- NETCONF RPC REPLY ---")
            print(pretty_xml(reply.xml))
            print("--- END RPC REPLY ---\n")

            if "<ok/>" in reply.xml or "<ok" in reply.xml:
                print("[SUCCESS] NETCONF reply contains <ok/>")
            else:
                print("[WARNING] No clear <ok/> found. Check reply manually.")

            get_running_config(m, "6 AFTER DEPLOYMENT")

    except RPCError as e:
        print("[NETCONF ERROR]")
        print(e)
        sys.exit(1)

    except Exception as e:
        print("[CONNECTION / SCRIPT ERROR]")
        print(e)
        sys.exit(1)


def main():
    print("==========================================")
    print(" IOS-XE NETCONF YANG Automation Project")
    print(" Luca Saltalamacchia")
    print("==========================================")
    print("Start time:", datetime.now())
    print()

    config_xml = get_config_from_github()
    payload = build_payload(config_xml)
    deploy_config(payload)

    print("DONE - DEPLOYMENT SUCCESSFUL")


if __name__ == "__main__":
    main()
