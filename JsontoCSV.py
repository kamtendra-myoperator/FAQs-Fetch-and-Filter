import json
import csv
def json_to_csv(json_file, csv_file):
    # Read JSON data from file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)['data']
    # Extract keys for CSV header
    header = ['Question', 'Answer', 'Category']
    # Write to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
# Provide the path to your JSON file
json_file = r"Categorised_FAQs.json"
# Convert JSON to CSV
json_to_csv(json_file, r"50_Categorised_FAQs.csv")