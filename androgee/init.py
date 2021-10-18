import requests
import sys
import os
from typing import Set

global swear_list
swear_list: Set = set(requests.get(
    "https://raw.githubusercontent.com/advaithm/badwords/master/badwords.json"
).json())
# I think it'd be better if we check if environment
# variables are present before doing anything else.
if os.path.exists(".env"):
    from dotenv import load_dotenv

    load_dotenv()
try:
    env = (
        os.environ
    )  # calling this for each value recreates the dict which increases load time
    MOD_ROLE_ID = int(env["MOD_ROLE_ID"])
    MOD_ROLE_NAME = env["MOD_ROLE_NAME"]
    COMMAND_PREFIX = env["DISCORD_PREFIX"]
    BOT_TOKEN = env["DISCORD_TOKEN"]
except KeyError as e:
    sys.exit(f"The {e} environment variable is missing! Androgee cannot run!")
