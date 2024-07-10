from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model for mistral or Llama3
llm = ChatOllama(model="mistral")

def detect_serial_killer(text):
    # Example with explicit labels included in the prompt
    example = "Phrase: 'Je vais te tuer, tu ne le mérites pas.' Classification: Tueur en série"
    prompt_template = ChatPromptTemplate.from_template(
        f"Classifiez les phrases suivantes dans l'une de ces catégories : Tueur en série, Non tueur en série.\n{example}\nPhrase: '{{text}}' Classification:"
    )

    # Combine the components into a chain
    chain = prompt_template | llm | StrOutputParser()

    # Invoke the chain to classify the new text
    result = chain.invoke({'text': text})
    # Extract the classification from the result
    classification = result.split("(")[0].strip()
    return classification

# Test the serial killer detection
test_sentence = "Je sais où tu es. Ne t'éloigne pas."
result = detect_serial_killer(test_sentence)
print(f"Résultat de la classification : {result}")