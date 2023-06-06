import re

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

# Usage
input_filename = "output.txt"  # Replace with the actual input filename
output_filename = "numbered_questions.txt"  # Replace with the desired output filename
number_questions(input_filename, output_filename)
