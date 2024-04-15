import json

# Load the JSON data from file
with open('combined_faqs_filtered_R1.json', 'r') as file:
    data = json.load(file)

# Sort the data based on the "Question" key
sorted_data = sorted(data['data'], key=lambda x: x['Question'])

# Save the sorted data to another JSON file
with open('sorted_combined_faqs_filtered_R1.json', 'w') as file:
    json.dump({'data': sorted_data}, file, indent=4)
