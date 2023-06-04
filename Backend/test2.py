import random
import re

def generate_questions(note):
    # Split the note into paragraphs
    paragraphs = note.split('\n\n')

    # Generate questions from the paragraphs
    questions = []
    for paragraph in paragraphs:
        # Split the paragraph into sentences
        sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())

        # Generate questions based on sentence structure
        for i in range(len(sentences)):
            sentence = sentences[i].strip()
            if sentence:
                if i == 0:
                    # Start with a general question about the paragraph
                    question = "What is the main topic of this paragraph?"
                elif i == len(sentences) - 1:
                    # End with a reflection or summary question
                    question = "What are the key takeaways from this paragraph?"
                else:
                    # Generate a random question related to the content of the sentence
                    question = generate_random_question(sentence)
                
                questions.append(question)

    # Shuffle the order of the questions
    random.shuffle(questions)

    return questions

def generate_random_question(sentence):
    # Implement your logic to generate a random question based on the content of the sentence
    # Here's a simple example that generates a generic question
    return "What can you infer from the statement: '" + sentence + "'?"

# Example usage
note = """
Chapter 1: Introduction to Biology

Biology is the study of living organisms. It encompasses various aspects such as the structure, function, growth, origin, evolution, and distribution of organisms.

Cell Theory states that all living organisms are composed of cells, which are the basic structural and functional units of life.

DNA, or deoxyribonucleic acid, carries the genetic information of an organism and is responsible for transmitting hereditary traits.

"""

questions = generate_questions(note)
for question in questions:
    print(question)
