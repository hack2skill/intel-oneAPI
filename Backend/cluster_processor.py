import re

def remove_extra_whitespace(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Remove unwanted characters before numbering
    content = re.sub(r'(?<=\n)\s*-+\s*', '', content)

    # Remove Roman numbering and add decimal numbering
    decimal_number = 1
    content = re.sub(r'(?<=\n)([IVXLCDM]+\.)(?=\s)', lambda match: str(decimal_number) + '.', content)
    decimal_number += 1

    # Remove extra white spaces
    content = re.sub(' +', ' ', content)

    with open(output_file, 'w') as file:
        file.write(content)


def number_questions(input_filename, output_filename):
    section_count = 0
    question_count = 0
    current_section = ""

    with open(input_filename, 'r') as input_file:
        lines = input_file.readlines()

    with open(output_filename, 'w') as output_file:
        for line in lines:
            # Check if the line starts with "Module X:"
            if re.match(r'^Module \d+:', line):
                section_count += 1
                question_count = 0
                current_section = re.findall(r'^Module \d+', line)[0]
                output_file.write(line)
            # Check if the line starts with "1.", "(a)", or "(i)"
            elif re.match(r'^\d+\.|^[(a-z)]\.|^[(i)]\.', line):
                question_count += 1
                # Modify the line to include the correct question number
                modified_line = re.sub(r'^(\d+\.|^[(a-z)]\.|^[(i)]\.)', str(question_count) + '.', line)
                # Replace the section number if necessary
                modified_line = modified_line.replace(current_section, 'Module ' + str(section_count))
                output_file.write(modified_line)
            else:
                output_file.write(line)


# Usage example
input_file = 'Local_Storage\Generated_Files\cluster_questions.txt'  # Replace with your input file path
temp_file = 'temp_output.txt'  # Replace with a temporary output file path
output_file = 'final_output.txt'  # Replace with your final output file path

# Step 1: Remove extra whitespace
remove_extra_whitespace(input_file, temp_file)

# Step 2: Number the questions
number_questions(temp_file, output_file)

# Step 3: Clean up the temporary file
import os
os.remove(temp_file)
