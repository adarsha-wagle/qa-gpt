import os

# Define the directory paths
qa_folder = 'question-answer'
output_folder = 'llama3'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def get_llama3_chat_template(messages):
    return (
        "<|begin_of_text|>\n"
        + "".join(
            f"<|start_header_id|>{message['role']}<|end_header_id|>\n{message['content']}\n<|eot_id|>\n"
            for message in messages
        )
        + "<|end_of_text|>"
    )

# Function to process Q&A pairs from a single file content
def process_qa_content(content):
    qas = []
    qa_pairs = [pair.strip() for pair in content.strip().split('\n\n') if pair.strip()]  # Skip empty lines
    for pair in qa_pairs:
        if pair.startswith("Q:"):
            question_answer = pair.split('A:')
            question = question_answer[0].replace('Q:', '').strip()
            answer = question_answer[1].strip() if len(question_answer) > 1 else ''  # Check if 'A:' tag exists
            qas.append({"role": "user", "content": question})
            qas.append({"role": "assistant", "content": answer})
    return qas

# Iterate over all files in the question-answer folder
for qa_filename in os.listdir(qa_folder):
    # Construct full file paths
    qa_path = os.path.join(qa_folder, qa_filename)
    output_path = os.path.join(output_folder, qa_filename)

    # Read Q&A content
    with open(qa_path, 'r') as qa_file:
        qa_content = qa_file.read().strip()

    # Process Q&A content into the required format
    qas = process_qa_content(qa_content)

    # Add the system message at the beginning
    messages = [{"role": "system", "content": "You are a helpful AI assistant for cybersecurity and threats"}] + qas

    # Convert content to LLaMA3 format using the template function
    llama3_content = get_llama3_chat_template(messages)

    # Save the formatted content to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(llama3_content)

    print(f'Formatted content saved to {output_path}')

print('All files have been processed and saved in the llama3 folder.')