import requests
import sys
import os

global swear_list
swear_list = requests.get(
    "https://raw.githubusercontent.com/advaithm/badwords/master/badwords.json"
).json()
# I think it'd be better if we check if environment
# variables are present before doing anything else.
if os.path.exists(".env"):
    from dotenv import load_dotenv

    load_dotenv()
try:
    MOD_ROLE_ID = os.environ["MOD_ROLE_ID"]
    MOD_ROLE_NAME = os.environ["MOD_ROLE_NAME"]
    COMMAND_PREFIX = os.environ["DISCORD_PREFIX"]
    BOT_TOKEN = os.environ["DISCORD_TOKEN"]
except KeyError as e:
    print(f"The {e} environment variable is missing! Androgee cannot run!")
    sys.exit(1)
