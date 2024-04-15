import os

def remove_slashes_in_files(input_directory, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get a list of all files in the input directory
    files = os.listdir(input_directory)

    # Iterate through each file
    for filename in files:
        # Check if the file is a text file
        if filename.endswith('.json'):
            input_filepath = os.path.join(input_directory, filename)
            output_filepath = os.path.join(output_directory, filename)
            
            with open(input_filepath, 'r') as file:
                # Read the content of the file
                content = file.read()
            
            # Remove slashes from the content
            cleaned_content = content.replace('/n', '').replace('/', '').replace('\\', '')

            # Change the format of the content from "[{},{},{}]" to [{},{},{}]
            cleaned_content = cleaned_content.replace('"[', '[').replace(']"', ']')

            # Replace ' with "
            cleaned_content = cleaned_content.replace("'Question': '", '"Question": "').replace("'Answer': '", '"Answer": "').replace("', '", '", "').replace("'}", '"}').replace("'}]", '"}]').replace("'," , '", ').replace('"Question": \'', '"Question": "').replace('"Answer": \'', '"Answer": "').replace("'Question'", '"Question"').replace("'Answer'", '"Answer"').replace('"Question\'', '"Question"').replace('"Answer\'', '"Answer"')

            #remove anything before [
            cleaned_content = cleaned_content.split("[",1)[1]

            #remove anything after ]
            cleaned_content = cleaned_content.rsplit("]",1)[0]

            # Write the cleaned content to the output file
            with open(output_filepath, 'w') as file:
                file.write(cleaned_content)

# Specify the input and output directories
input_directory = 'R1_Filtered_FAQs'
output_directory = 'R1_Cleaned_FAQs'

# Call the function to remove slashes from files in the input directory
remove_slashes_in_files(input_directory, output_directory)