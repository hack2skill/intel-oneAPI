from pprint import pprint


def process_file(file_path):
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process the lines
    processed_data = {}
    current_section = None
    current_subsection = None
    current_questions = []
    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Check if it's a section
        if line.startswith("PART"):
            current_section = line
            processed_data[current_section] = []
            current_subsection = None
            current_questions = []
            continue

        # Check if it's a subsection
        if line.startswith(("I.", "II.", "III.", "IV.", "V.", "VI.", "VII.", "VIII.", "IX.")):
            current_subsection = line
            current_questions = []
            continue

        # Add question to the current subsection's questions
        if current_subsection:
            current_questions.append(line)

        # Check if it's the end of a subsection
        if line.startswith("***"):
            if current_section and current_subsection:
                processed_data[current_section].append({'subsection': current_subsection, 'questions': current_questions})
                current_subsection = None
                current_questions = []

    # Print debug information
    print("Processed Data:")
    pprint(processed_data)

    # Format the extracted information
    formatted_data = ''
    for section, subsections in processed_data.items():
        formatted_data += section + '\n\n'
        for subsection_data in subsections:
            formatted_data += subsection_data['subsection'] + '\n'
            formatted_data += '\n'.join(subsection_data['questions']) + '\n\n'

    # Save the processed data
    output_file_path = file_path + '_processed.txt'
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(formatted_data)
        print(f"Processing complete. Processed data saved to: {output_file_path}")
    except Exception as e:
        print("Error occurred while saving processed data:")
        print(str(e))


# Usage: Provide the file path as a parameter to the process_file function
process_file('Local_Storage\pyqs_text\qp.txt')
