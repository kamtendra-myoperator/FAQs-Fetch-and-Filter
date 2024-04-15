import json
from openai import OpenAI
import os
from fpdf import FPDF

def generate_questions_and_answers(result_string):
    system_content = '''You are a category assigner and you will be given a JSON having question and answer in this format: \n
    {"data":[{"Question":"<Question>","Answer":"<Answer>"},{"Question":"<Question>","Answer":"<Answer>"}]} \n
    The goal is to assign category to each question answer pair with extra field "Category". \n
    Available Categories: \n
    1. Plans and invoices
    2. Calling related
    3. WhatsApp related
    4. General queries/Others
    5. Account deactivation
    6. Account creation /onboarding \n
    Always return the data in JSON format given {"data":[{"Question":"<Question>","Answer":"<Answer>","Category":"<Category>"},{"Question":"<Question>","Answer":"<Answer>","Category":"<Category>"}]}'''

    client = OpenAI(api_key="YOUR_API_KEY")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can adjust the model based on your preference
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": result_string}
        ]
    )

    print(type(completion.choices[0].message.content))
    # Parse the completion and extract questions and answers
    content_json = json.loads(completion.choices[0].message.content)
    qa_pairs = []
    for qa in content_json['data']:
        qa_pairs.append({'Question': qa['Question'], 'Answer': qa['Answer'], 'Category': qa['Category']})

    return qa_pairs

    # print(completion.choices[0].message.content)
    # return completion.choices[0].message.content

def process_conversation_folder(folder_path):
    # Process each conversation file in the folder
    faqs = []
    check=1
    for filename in os.listdir(folder_path):
        print(check)
        print(filename)
        check+=1
        if check==50:
            break
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                conversation_text = file.read()
        
            # Generate questions and answers from conversation text
            conversation_faqs = generate_questions_and_answers(conversation_text)
            faqs.extend(conversation_faqs)

    return faqs

def main():
    # Define the initial JSON data structure
    initial_data = {'data': []}

    # Create the initial JSON file with empty data
    output_file = 'Categorised_FAQs.json'
    with open(output_file, 'w') as f:
        json.dump(initial_data, f, indent=4)

    # Define the folder containing conversation transcripts
    folders = ['R2_Filered_FAQs_Chunks_of_25']  # Update with your folder paths

    # Process each folder and append FAQs to the existing JSON data
    for folder in folders:
        faqs = process_conversation_folder(folder)
        if faqs:
            # Append FAQs to the existing JSON data
            with open('Categorised_FAQs.json', 'r+') as f:
                existing_data = json.load(f)
                existing_data['data'].extend(faqs)
                f.seek(0)  # Move to the beginning of the file
                json.dump(existing_data, f, indent=4)
                f.truncate()  # Clear any remaining content if FAQs are shorter than existing data

if __name__ == "__main__":
    main()
