import sys
import requests

# For authorization, you can use either your bot token
headers = {"authorization": "Bot MTA4MDYwNDUxNTM5MDIxMDEzOQ.GBogcX.tV3lBnPZjP4g-7kxyfW6yHvz5dKeH1i3D0E6io"}

r = requests.get("https://discord.com/api/v10/applications/1080604515390210139/guilds/772577481919430656/commands", headers=headers)

url = "https://discord.com/api/v10/applications/1080604515390210139/guilds/772577481919430656/commands"

# This is an example USER command, with a type of 2
json = {
    "name": "high-five",
    "type": 3
}

r = requests.post(url, headers=headers, json=json)
