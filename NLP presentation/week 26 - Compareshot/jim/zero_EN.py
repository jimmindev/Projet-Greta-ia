# Import the necessary modules from the Langchain library
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model for Mistral
# This model will be used to classify the texts
llm = ChatOllama(model="mistral")

# Define the zero-shot classification function
def detect_serial_killer(text):
    # Define the prompt with an explicit instruction for classification
    # The prompt includes placeholders for the text to be classified and the categories
    prompt_template = ChatPromptTemplate.from_template(
        "Does the following text mention a serial killer? Answer 'Serial Killer' if it does, and 'Non-Serial Killer' if it doesn't. Just give me exactly the predicted label without any opening or closing statement from you: '{text}'"
    )

    # Combine the components into a chain
    # The chain consists of the prompt template, the language model, and an output parser
    chain = prompt_template | llm | StrOutputParser()

    # Invoke the chain to execute the classification task
    # The text is passed as an input to the chain, which returns the predicted category
    result = chain.invoke({'text': text})
    return result

# Define a text related to detecting serial killers in English
text = "The suspect has a history of violence, including assault and threats. However, there is no evidence to suggest that he has committed any murders."

# Detect whether the text mentions a serial killer and print the result
result = detect_serial_killer(text)
#print(f"The text '{text}' is classified as: {result}")
print(f"Classified as: {result}")