from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="mistral")

def detect_serial_killer(text):
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
    result_dict = json.loads(result)
    return json.dumps(result_dict)

# Test the serial killer detection
test_sentence = "Hello"
result = detect_serial_killer(test_sentence)
formatted_result = json.dumps(json.loads(result), indent=4, ensure_ascii=False)
print(f"{formatted_result}")