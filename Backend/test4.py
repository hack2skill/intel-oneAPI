import re

# Read input from text file
with open('question_papers/cluster_questions.txt', 'r') as file:
    text = file.read()

# Remove old numbering and add decimal numbering
lines = text.split('\n')
module_questions = {}
current_module = None
question_number = 1

for line in lines:
    if line.startswith('Module'):
        current_module = re.findall(r'\d+', line)[0]
        module_questions[current_module] = []
        question_number = 1
    elif line.strip().startswith('-'):
        question = line.strip()[1:].strip()
        if question.startswith('('):
            question = question[1:].strip()
        question = re.sub(r'^[IVX]+\.?\s*', str(question_number) + '. ', question)
        module_questions[current_module].append(question)
        question_number += 1

# Save module questions to a file
with open('module_questions.txt', 'w') as file:
    for module, questions in module_questions.items():
        file.write(f"Module {module}:\n")
        for question in questions:
            file.write(f"{question}\n")

print("Module questions saved to 'module_questions.txt' file.")
