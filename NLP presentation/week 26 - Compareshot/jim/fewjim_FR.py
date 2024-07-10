from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import json

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="mistral")

def detect_serial_killer(text):
    # Définir le modèle de message système avec les exemples inclus
    system_template = """Vous êtes un assistant qui classe les phrases dans les catégories suivantes : Tueur en série, Non tueur en série, Tueur Shiny Vmax. Voici des exemples :
    - Phrase: 'Je suis ravie de faire partie de cela !' Classification: Non tueur en série
    - Phrase: 'C'est inacceptable, j'exige une explication !' Classification: Non tueur en série
    - Phrase: 'Je vais te tuer, tu ne le mérites pas.' Classification: Tueur en série
    - Phrase: 'Bonjour' Classification: Tueur Shiny Vmax
    - Phrase: 'Je veux juste profiter de ma journée.' Classification: Non tueur en série
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # Définir le modèle de message humain
    human_template = "Phrase: '{text}'. Classifiez cette phrase dans l'une de ces catégories : Tueur en série, Non tueur en série, Tueur Shiny Vmax. Veuillez me donner la sortie sous forme de dictionnaire avec la phrase et la classification prédite sans aucun commentaire de votre part."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Combiner les modèles de message en un modèle de chat
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Combine les composants en une chaîne
    chain = chat_prompt | llm | StrOutputParser()

    # Invoquer la chaîne pour classifier le nouveau texte
    result = chain.invoke({'text': text})
    result_dict = json.loads(result)
    # print(result_dict)
    return result_dict

# Tester la détection de tueur en série
test_sentence = "Bonjour"
result = detect_serial_killer(test_sentence)
formatted_result = json.dumps(result, indent=4 , ensure_ascii=False)
print(f"{formatted_result}")