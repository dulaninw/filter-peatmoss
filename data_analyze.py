import json
import openai
import os

# Loading the API key securely from an environment variable

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

filename = ''


data = load_json(filename)
all_messages = " ".join([commit['message'] for commit in data])

# questions you want to ask about the data
questions = [
    "When is a PTM added to a project? What new task is it filling?",
    "How are new changes to a PTM reflected in its downstream usage? Is a new PTM that performs the same task as an old PTM but with higher performance ever considered?",
    "When is a PTM removed from a project? Does anything on the PTM end cause it to be abandoned?"
]

for question in questions:

    enhanced_prompt = f"Given the GitHub project at {all_messages} which includes commit changes such as device handling in the script, consider the following question based on the PR discussions related to PTM usage:"
    prompt_text = enhanced_prompt + " " + question
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=250
    )
    print("Question:", question)
    print("Answer:", response.choices[0].message['content'].strip())
    print("--------")