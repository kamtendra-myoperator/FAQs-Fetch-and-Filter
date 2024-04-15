import json
import os

# Directory containing the JSON files
directory = 'Final_Filtered_And_Formatted_JSon_Files'

# List to hold combined data
combined_data = {"data": []}

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as file:
            # Load JSON data from file
            data = json.load(file)
            # Extend the combined data list with the data from the current file
            combined_data["data"].extend(data["data"])

# Write the combined data to a new JSON file
output_file = 'combined_faqs_filtered_R1.json'
with open(output_file, 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)

print(f"Combined data written to {output_file}")
