from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json
import pandas as pd

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="mistral")

# Zero-Shot Function
def classify_text(text):
    # Define the prompt with an explicit instruction for classification
    prompt_template = ChatPromptTemplate.from_template(
        "Does the following text mention a serial killer? Answer 'Serial Killer' if it does, and 'Non-Serial Killer' if it doesn't. Just give me exactly the predicted label without any opening or closing statement from you: '{text}'"
    )

    # Combine the components into a chain
    chain = prompt_template | llm | StrOutputParser()

    # Invoke the chain to execute the classification task
    result = chain.invoke({'text': text})
    return result

# One shot
def one_shot_classify(text):
    # Example with explicit labels included in the prompt
    example = "Sentence: 'I am going to kill you, you don't deserve it.' Classification: Serial Killer"
    prompt_template = ChatPromptTemplate.from_template(
        f"Classify the following sentences into one of these categories: Serial Killer, Non-Serial Killer.\n{example}\nSentence: '{{text}}' Classification:"
    )

    # Combine the components into a chain
    chain = prompt_template | llm | StrOutputParser()

    # Invoke the chain to classify the new text
    result = chain.invoke({'text': text})
    # Extract the classification from the result
    classification = result.split("(")[0].strip()
    return classification

# Few shot
def few_shot_classify(text):
    # Define the system message template with examples included
    system_template = """You are an assistant that classifies phrases into the following categories: Serial Killer, Non-Serial Killer, Shiny Vmax Killer. Here are some examples:
    - Phrase: 'I am thrilled to be part of this!' Classification: Non-Serial Killer
    - Phrase: 'This is unacceptable, I demand an explanation!' Classification: Non-Serial Killer
    - Phrase: 'I am going to kill you, you don't deserve it.' Classification: Serial Killer
    - Phrase: 'Hello' Classification: Shiny Vmax Killer
    - Phrase: 'I just want to enjoy my day.' Classification: Non-Serial Killer
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # Define the human message template
    human_template = "Phrase: '{text}'. Classify this phrase into one of the following categories: Serial Killer, Non-Serial Killer, Shiny Vmax Killer. Please give me the output as a dictionary with the phrase and the predicted classification, without any opening or closing statement from you."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Combine the message templates into a chat template
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Combine the components into a chain
    chain = chat_prompt | llm | StrOutputParser()

    # Invoke the chain to classify the new text
    result = chain.invoke({'text': text})

    # Debugging: print the raw result
    print(f"Raw result: {result}")

    try:
        result_dict = json.loads(result)
    except json.JSONDecodeError:
        # Handle the error gracefully by returning a default or indicating an error
        result_dict = {"Phrase": text, "Classification": "Error"}
    
    return json.dumps(result_dict)

# Load the dataset
df = pd.read_csv('synthetic_phrases_serial_killer.csv')

# Apply the classification functions
df['Zero_Shot'] = df['Phrase'].apply(classify_text)
df['One_Shot'] = df['Phrase'].apply(one_shot_classify)
df['Few_Shot'] = df['Phrase'].apply(few_shot_classify)

print(df)
df.to_csv('synthetic_customer_chats.csv', index=False)

# Comparing the performance

def calculate_accuracy(df, column):
    return (df[column] == df['Category']).mean()

zero_shot_accuracy = calculate_accuracy(df, 'Zero_Shot')
one_shot_accuracy = calculate_accuracy(df, 'One_Shot')
few_shot_accuracy = calculate_accuracy(df, 'Few_Shot')

print(f"Zero-Shot Accuracy: {zero_shot_accuracy}")
print(f"One-Shot Accuracy: {one_shot_accuracy}")
print(f"Few-Shot Accuracy: {few_shot_accuracy}")