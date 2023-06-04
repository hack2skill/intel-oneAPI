import re

# Read input from text file
with open('question_papers/cluster_questions.txt', 'r') as file:
    text = file.read()

# Extract module numbers and questions
module_questions = {}
current_module = None

lines = text.split('\n')
for line in lines:
    if line.startswith('Module'):
        current_module = re.findall(r'\d+', line)[0]
        module_questions[current_module] = []
    elif line.strip().startswith('-'):
        question = line.strip()[1:].strip()
        question = re.sub(r'(\.\s+)', '. ', question)
        module_questions[current_module].append(question)

# Save module questions to a file
with open('question_papers/module_questions.txt', 'w') as file:
    for module, questions in module_questions.items():
        file.write(f"Module {module}:\n")
        for question in questions:
            file.write(f"- {question}\n")

print("Module questions saved to 'module_questions.txt' file.")
