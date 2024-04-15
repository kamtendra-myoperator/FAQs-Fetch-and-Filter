import os
import json

# Load the JSON data
with open('testdup.json', 'r') as f:
    faq_data = json.load(f)

# If the loaded data is not a list, assume it's a dictionary with a key 'data'
if not isinstance(faq_data, list):
    faq_data = faq_data.get('data', [])

# Create a folder to save the files
folder_name = 'R2_Filered_FAQs_Chunks_of_25'
os.makedirs(folder_name, exist_ok=True)

# Define the chunk size
chunk_size = 25

# Initialize variables
chunk_count = 1
current_chunk = {"data": []}

# Split data into chunks and save each chunk as a separate file
for item in faq_data:
    current_chunk["data"].append(item)
    if len(current_chunk["data"]) == chunk_size:
        # Save the chunk to a file
        file_name = os.path.join(folder_name, f"{chunk_count}.json")
        with open(file_name, "w") as f:
            json.dump(current_chunk, f, indent=4)
        # Reset current chunk and increment chunk count
        current_chunk = {"data": []}
        chunk_count += 1

# Save the remaining items as a separate chunk if any
if current_chunk["data"]:
    file_name = os.path.join(folder_name, f"{chunk_count}.json")
    with open(file_name, "w") as f:
        json.dump(current_chunk, f, indent=4)

print("Files saved successfully.")
