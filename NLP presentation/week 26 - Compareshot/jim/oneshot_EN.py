from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model for mistral or Llama3
llm = ChatOllama(model="mistral")

def detect_serial_killer(text):
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

# Test the serial killer detection
test_sentence = "I have been waiting for you all night. Come out now."
result = detect_serial_killer(test_sentence)
print(f"Classification Result: {result}")