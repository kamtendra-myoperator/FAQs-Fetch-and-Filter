import os
import json
from langchain_openai import ChatOpenAI

def filter_faqs(json_data):
    llm = ChatOpenAI(openai_api_key="YOUR_API_KEY", model="gpt-3.5-turbo-0613")
    
    response = llm.invoke(f"Please filter out the faqs which have name of other companies than Heyo. Here is the data: \n {json_data} \n Always only return the json data only and only even if the data is already filtered and do not return extra text other than json.")

    return response.content

def filter_multiple_files(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through each file in the input folder
    for i in range(179,201):
        filename = f"{i}.json"
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            # Open and load JSON data from input file
            with open(input_file_path, 'r+') as file:
                json_data = json.load(file)
            
            # Filter FAQs
            filtered_faqs = filter_faqs(json_data)
            
            # Save filtered JSON data to output file in the desired format
            with open(output_file_path, 'w') as file:
                json.dump(filtered_faqs, file, indent=4)
                
            print(f"Filtered file saved: {output_file_path}")

# Example usage:
input_folder = 'FAQS_Chunks_of_25'
output_folder = 'R1_Filtered_FAQs'
filter_multiple_files(input_folder, output_folder)
