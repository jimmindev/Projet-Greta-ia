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
        "Le texte suivant mentionne-t-il un tueur en série ? Répondez 'tueur en série' s'il le fait, et 'pas tueur en série' s'il ne le fait pas. Donnez-moi uniquement l'étiquette prédite sans aucune ouverture ou fermeture de déclaration de votre part : '{text}'"
    )

    # Combine the components into a chain
    # The chain consists of the prompt template, the language model, and an output parser
    chain = prompt_template | llm | StrOutputParser()

    # Invoke the chain to execute the classification task
    # The text is passed as an input to the chain, which returns the predicted category
    result = chain.invoke({'text': text})
    return result

# Define a text related to detecting serial killers in French
text = "Le suspect a une histoire de violence, y compris d'agression et de menaces. Cependant, il n'y a aucune preuve pour suggérer qu'il a commis des meurtres."

# Detect whether the text mentions a serial killer and print the result
result = detect_serial_killer(text)
#print(f"Le texte '{text}' est classé comme : {result}")
print(f"Classé comme : {result}")