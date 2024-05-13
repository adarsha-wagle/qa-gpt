import os
from openai import OpenAI
from secret import api_key

client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key
)
def saveQAPairs (qa_pairs,question_and_answer_folder,file_name):
    qa_folder = os.path.join(question_and_answer_folder)
    if not os.path.exists(qa_folder):
        os.makedirs(qa_folder)
    with open(os.path.join(qa_folder,f"{file_name}_qa.txt"), 'w') as f:
        for i in range(0, len(qa_pairs), 2):
            if i + 1 < len(qa_pairs):
                f.write(f" {qa_pairs[i]}\n")
                f.write(f" {qa_pairs[i + 1]}\n\n")
            else:
                print(f"Missing answer for question: {qa_pairs[i]}")
                
    print (f"QA File {file_name} saved")

def cleanAndSave(input_folder,cleaned_folder):
    print ("Cleaning up unwanted spacing",end="")
    try:
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):
                with open(os.path.join(input_folder, filename), 'r') as file:
                    content = file.read()

                cleaned_content = " ".join(content.split())

                with open(os.path.join(cleaned_folder, filename), 'w') as file:
                    file.write(cleaned_content)

        print("File Cleaned and Saved")
    except : 
        print("Failed to clean")
        continue
        

def generateQA(cleaned_folder,question_and_answer_folder):
    print ("Generating QA Hold On",end="")
    for file_name in os.listdir(cleaned_folder):
        if file_name.endswith('.txt'):
            with open(os.path.join(cleaned_folder, file_name), 'r') as file:
                content = file.read()
            # print (content)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": content + "Can you generate question and answer by reading this content",
                    }
                ],
                model="gpt-3.5-turbo",
            )
        choices = chat_completion.choices
        message = choices[0].message.content
        qa_pairs = message.strip().split("\n")
        saveQAPairs (qa_pairs,question_and_answer_folder,file_name)  
                
def main(input_folder,cleaned_folder,question_and_answer_folder):
    cleanAndSave(input_folder,cleaned_folder)
    generateQA(cleaned_folder,question_and_answer_folder
)
    
   

if __name__ == "__main__":
    input_folder = "defend-mitre/data/"
    cleaned_folder = "cleaned/"
    question_and_answer_folder = "question-answer/"
    # Create  cleaned folder if it doesn't exist
    if not os.path.exists(cleaned_folder):
        os.makedirs(cleaned_folder)
    # Create  question-and-answer folder if it doesn't exist
    if not os.path.exists(question_and_answer_folder
):
        os.makedirs(question_and_answer_folder
    )
    main(input_folder,cleaned_folder,question_and_answer_folder
)