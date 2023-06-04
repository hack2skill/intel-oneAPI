import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the pre-trained model and tokenizer
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def generate_model_questions(input_questions, num_questions=1):
    # Encode input questions
    input_ids = tokenizer.encode(input_questions, return_tensors='pt')

    # Generate model questions
    max_length = 512  # Adjust the maximum length of the generated questions
    temperature = 1.0  # Adjust the temperature for controlling randomness

    model_questions = []
    for _ in range(num_questions):
        outputs = model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            temperature=temperature,
            repetition_penalty=1.0,
            pad_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )

        # Decode the generated model question
        model_question = tokenizer.decode(outputs[0], skip_special_tokens=True)
        model_questions.append(model_question)

    return model_questions

# Example usage
input_questions = """1. Explain the design procedure of combinational circuit with an example
2. Implement the following function using a multiplexer
3. Compare TTL and CMOS logic families.
4. Implement the following Boolean function with NAND gates: OR
5. Implement the following function using a multiplexer (Use B as input)"""
model_questions = generate_model_questions(input_questions)

print("Input Question:")
print(input_questions)
print("\nModel Questions:")
for i, question in enumerate(model_questions, 1):
    print(f"{i}. {question}")
