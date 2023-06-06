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

# Usage example
input_file = 'Local_Storage\Generated_Files\cluster_questions.txt'  # Replace with your input file path
output_file = 'output.txt'  # Replace with your output file path
remove_extra_whitespace(input_file, output_file)
