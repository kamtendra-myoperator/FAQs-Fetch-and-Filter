import json
import requests
import sys
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()


def save_conversation(conversation_id, current_file_index, conversation_count):
    # Define the API endpoint and headers
    url = f'https://myoperator.freshchat.com/v2/conversations/{conversation_id}/messages?items_per_page=50'
    headers = {
        'Authorization': f'Bearer eyJraWQiOiJjdXN0b20tb2F1dGgta2V5aWQiLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmcmVzaGNoYXQiLCJzdWIiOiI0NzUxNTJmNC0wYjU4LTQ3YjItOWJlZS01OGNhOTUyMTNlNDkiLCJjbGllbnRJZCI6ImZjLWE2ZThiOGRiLWRmZWMtNGE1Ni04YWVlLWY0OTEwMWVkMWI3NCIsInNjb3BlIjoiYWdlbnQ6cmVhZCBhZ2VudDpjcmVhdGUgYWdlbnQ6dXBkYXRlIGFnZW50OmRlbGV0ZSBjb252ZXJzYXRpb246Y3JlYXRlIGNvbnZlcnNhdGlvbjpyZWFkIGNvbnZlcnNhdGlvbjp1cGRhdGUgbWVzc2FnZTpjcmVhdGUgbWVzc2FnZTpnZXQgYmlsbGluZzp1cGRhdGUgcmVwb3J0czpmZXRjaCByZXBvcnRzOmV4dHJhY3QgcmVwb3J0czpyZWFkIHJlcG9ydHM6ZXh0cmFjdDpyZWFkIGFjY291bnQ6cmVhZCBkYXNoYm9hcmQ6cmVhZCB1c2VyOnJlYWQgdXNlcjpjcmVhdGUgdXNlcjp1cGRhdGUgdXNlcjpkZWxldGUgb3V0Ym91bmRtZXNzYWdlOnNlbmQgb3V0Ym91bmRtZXNzYWdlOmdldCBtZXNzYWdpbmctY2hhbm5lbHM6bWVzc2FnZTpzZW5kIG1lc3NhZ2luZy1jaGFubmVsczptZXNzYWdlOmdldCBtZXNzYWdpbmctY2hhbm5lbHM6dGVtcGxhdGU6Y3JlYXRlIG1lc3NhZ2luZy1jaGFubmVsczp0ZW1wbGF0ZTpnZXQgZmlsdGVyaW5ib3g6cmVhZCBmaWx0ZXJpbmJveDpjb3VudDpyZWFkIHJvbGU6cmVhZCBpbWFnZTp1cGxvYWQiLCJpc3MiOiJmcmVzaGNoYXQiLCJ0eXAiOiJCZWFyZXIiLCJleHAiOjE5NzQ0NDQ3NjgsImlhdCI6MTY1ODgyNTU2OCwianRpIjoiNzg0MTgxMGItMzA0Mi00YjQ0LWE2NzUtNzI4YmFlYjliOWQ1In0.FkCNF8VQYM6qlkQOxz96Ky5RRGRiBvbuFcKKZn75p_g'
    }

    # Send GET request to the API
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON data
        data = response.json()

        # Filter out messages between agent and customer
        agent_customer_messages = [message for message in data['messages'] if ('actor_type' in message and message['actor_type'] == 'agent' and message['message_type'] == 'normal') or ('actor_type' in message and message['actor_type'] == 'user')]

        # Reverse the list to get messages in chronological order
        agent_customer_messages.reverse()

        # Extract text content of each message part for each message
        conversation = ''

        conversation +='\n' + 'Convesration ' + str(conversation_count) + ':\n\n'

        for message in agent_customer_messages:
            sender = 'Agent' if message['actor_type'] == 'agent' else 'Customer'
            message_content = ''
            for message_part in message['message_parts']:
                message_content += message_part['text']['content'] + '\n' if 'text' in message_part else ''
            conversation += f"{sender}: {message_content}\n"

        # Check if the conversation fits in the current file or if a new file is needed
        filename = os.path.join('conversations', f'conversation_{current_file_index}.txt')
        if os.path.exists(filename):
            # Read current file content to get the current character count
            with open(filename, 'r', encoding='utf-8') as file:
                current_content = file.read()
            current_char_count = len(current_content)
            if current_char_count + len(conversation) > 7000:
                # Create a new file if the conversation exceeds 7000 characters
                current_file_index += 1
                filename = os.path.join('conversations', f'conversation_{current_file_index}.txt')


        # Save conversation to TXT file with UTF-8 encoding
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(conversation)


        print(f"Conversation saved successfully to {filename}.")
        return current_file_index
    else:
        print("Failed to retrieve conversation data. Status code:", response.status_code)
        return current_file_index

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python script.py conversation_id1 conversation_id2 ...")
    #     sys.exit(1)

    # auth_token = os.getenv("AUTH_TOKEN")
    # if auth_token is None:
    #     print("Authorization token not found in .env file.")
    #     sys.exit(1)

    current_file_index = 1

    # Read conversation IDs from Excel sheet
    try:
        df = pd.read_excel(r"D:\Heyo FAQ\freshchat data.xlsx")
        conversation_ids = df['conversation_id'].tolist()[:1000]
    except Exception as e:
        print("Error reading Excel file:", e)
        sys.exit(1)

    # Create the conversations folder if it doesn't exist
    if not os.path.exists('conversations'):
        os.makedirs('conversations')


    conversation_count =0 

    for conversation_id in conversation_ids:
        conversation_count+=1
        current_file_index = save_conversation(conversation_id,  current_file_index, conversation_count)
