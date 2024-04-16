import asyncio
from datetime import datetime, timedelta, timezone
from telethon.sync import TelegramClient
from telethon.tl.types import Message
import time
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

def slow_colorful_print(text, color, delay):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL)

def save_credentials(api_id, api_hash):
    with open("credentials.txt", "w") as file:
        file.write(f"api_id={api_id}\n")
        file.write(f"api_hash={api_hash}\n")

async def main():
    # Check if credentials file exists
    if not os.path.isfile("credentials.txt"):
        print("This seems to be your first time running the tool.")
        print("Please provide your API credentials.")
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API hash: ")
        save_credentials(api_id, api_hash)
    else:
        # Read credentials from file
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = lines[0].strip().split("=")[1]
            api_hash = lines[1].strip().split("=")[1]
    
    # Ask user for group ID
    group_id = input("Enter the target group ID: ")
    
    # Initialize the Telegram client
    client = TelegramClient('session_name', api_id, api_hash)

    await client.start()
    
    # Print colored and animated text "MHA"
    slow_colorful_print("M   H   A", Fore.BLUE, 0.1)
    print()  # New line
    
    # Print colored options
    print(Fore.GREEN + "1 - " + Fore.YELLOW + "Last 24 hours")
    print(Fore.GREEN + "2 - " + Fore.YELLOW + "Last 48 hours")
    print(Fore.GREEN + "3 - " + Fore.YELLOW + "Last 1 week")
    
    # Reset text color to default
    choice = int(input("\033[0mEnter your choice (1/2/3): "))
    
    # Initialize an empty set to store unique user IDs
    user_ids = set()
    
    # Get the start date based on the user's choice
    if choice == 1:
        start_date = datetime.now(timezone.utc) - timedelta(hours=24)
    elif choice == 2:
        start_date = datetime.now(timezone.utc) - timedelta(hours=48)
    elif choice == 3:
        start_date = datetime.now(timezone.utc) - timedelta(weeks=1)
    else:
        print("\033[31mInvalid choice!")
        return
    
    async for message in client.iter_messages(int(group_id), limit=10000):
        if message.sender_id is not None and message.date >= start_date:
            if message.sender_id not in user_ids:
                user_ids.add(message.sender_id)
                print("\033[32mExtracted user ID - {}: {}".format(len(user_ids), message.sender_id))
    
    # Reset text color to default
    with open('user_ids.txt', 'w') as file:
        for user_id in user_ids:
            file.write(str(user_id) + '\n')

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
