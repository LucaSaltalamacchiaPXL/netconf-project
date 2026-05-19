from ncclient import manager

router = {
    "host": "10.0.2.15",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  </native>
</filter>
"""

with manager.connect(**router) as m:
    response = m.get_config(source="running", filter=netconf_filter)
    print(response.xml)
