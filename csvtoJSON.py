import csv
import json

def csv_to_json(csv_file, json_file):
    # Initialize an empty dictionary to hold the data
    data = {}

    # Open the CSV file and load data into the dictionary
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Assuming the first column contains the keys and the subsequent columns contain the values
            key = row[0]  # Use the first column as the key
            values = row[1:]  # Use the rest of the columns as values
            data[key] = values

    # Write the JSON data to a file
    with open(json_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Example usage:
csv_to_json('R2_Filtered_Combined_faqs.csv', 'testingjson.json')
