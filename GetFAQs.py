import json
from openai import OpenAI
import os
from fpdf import FPDF

def generate_questions_and_answers(result_string):
    system_content = '''You are a content creator tasked with generating general FAQs from conversations. 
    The goal is to extract commonly asked questions and their corresponding answers from the provided chat transcriptions. 
    Please ensure that the questions and answers are relevant to a broad audience and do not contain any user-specific information.
    Detailed Insructions:
    1. Review the chat transcriptions provided and extract commonly asked questions and their corresponding answers.
    2. Ensure that the generated FAQs are applicable to a wide audience and do not contain any user-specific details.
    3. Pay attention to recurring themes or topics in the conversations and formulate FAQs based on them.
    4. Provide concise and informative answers to each question, ensuring they are understandable by anyone.
    5. Exclude any personal or sensitive information from the FAQs and focus on general inquiries.
    6. Do not include Customers's company's information in the FAQs.
    Always return the data in JSON format given {"data":[{"Question":"<Question>","Answer":"<Answer>"},{"Question":"<Question>","Answer":"<Answer>"}]}'''

    client = OpenAI(api_key="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")

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
        check+=1
        if filename.endswith('.txt'):
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
    output_file = 'faqs10.json'
    with open(output_file, 'w') as f:
        json.dump(initial_data, f, indent=4)

    # Define the folder containing conversation transcripts
    folders = ['conversations9']  # Update with your folder paths

    # Process each folder and append FAQs to the existing JSON data
    for folder in folders:
        faqs = process_conversation_folder(folder)
        if faqs:
            # Append FAQs to the existing JSON data
            with open('faqs10.json', 'r+') as f:
                existing_data = json.load(f)
                existing_data['data'].extend(faqs)
                f.seek(0)  # Move to the beginning of the file
                json.dump(existing_data, f, indent=4)
                f.truncate()  # Clear any remaining content if FAQs are shorter than existing data

if __name__ == "__main__":
    main()