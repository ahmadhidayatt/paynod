from loguru import logger
from curl_cffi import requests
import pyfiglet
import time

# Set up logger format
logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=''),
    format="{time:DD/MM/YY HH:mm:ss} | <level>{level:8}</level> | <level>{message}</level>"
)

# main.py
def print_header():
    cn = pyfiglet.figlet_format("dailyclaim")
    print(cn)
    print("🌱 Season 2")
    print("🎨 by \033]8;;https://github.com/officialputuid\033\\officialputuid\033]8;;\033\\")
    print("✨ Credits: AirdropFamilyIDN")
    print('🎁 \033]8;;https://paypal.me/IPJAP\033\\Paypal.me/IPJAP\033]8;;\033\\ — \033]8;;https://trakteer.id/officialputuid\033\\Trakteer.id/officialputuid\033]8;;\033\\')

# Initialize the header
print_header()

# Read Tokens and Proxy count
def read_tokens():
    with open('tokens.txt', 'r') as file:
        tokens_content = sum(1 for line in file)
    return tokens_content

tokens_content = read_tokens()

# Print the token count
print()
print(f"🔑 Tokens: {tokens_content}.")
print()

def truncate_token(token):
    return f"{token[:4]}--{token[-4:]}"

# Function to claim reward using the provided token
def claim_reward(token):
    url = "https://api.nodepay.org/api/mission/complete-mission"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://app.nodepay.ai",
        "Referer": "https://app.nodepay.ai/"
    }
    data = {"mission_id": "1"}

    try:
        response = requests.post(url, headers=headers, json=data, impersonate="chrome110")

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('success'):
                logger.success(f"Token: {truncate_token(token)} | Reward claimed successfully")
            else:
                logger.info(f"Token: {truncate_token(token)} | Reward already claimed or another issue occurred")
        else:
            logger.error(f"Token: {truncate_token(token)} | Failed request, HTTP Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.exception(f"Token: {truncate_token(token)} | Request error: {e}")

def main():
    try:
        with open('tokens.txt', 'r') as file:
            tokens = file.read().splitlines()

        for token in tokens:
            claim_reward(token)

        # Send a final message after all operations are done
        logger.success(f"All tokens processed. Daily claim operation completed.")

    except FileNotFoundError:
        logger.error(f"The file 'tokens.txt' was not found. Please make sure it exists.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        while True:
            main()
            logger.info("Waiting 24 hours before the next run, ENJOY!")
            time.sleep(86400) # 86400s (24h)
    except (KeyboardInterrupt, SystemExit):
        logger.info(f"Program terminated by user. ENJOY!\n")
