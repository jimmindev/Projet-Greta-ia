from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model for mistral or Llama3
llm = ChatOllama(model="llama3")

def one_shot_classify(text):
    # Example with explicit labels included in the prompt
    example = "Sentence: 'I am thrilled to be part of this!' Classification: Happiness"
    prompt_template = ChatPromptTemplate.from_template(
        f"Classify the following sentences into one of these categories: Happiness, Sadness, Neutral.\n{example}\nSentence: '{{text}}' Classification:"
    )
    
    # Combine the components into a chain
    chain = prompt_template | llm | StrOutputParser()
    
    # Invoke the chain to classify the new text
    result = chain.invoke({'text': text})
    return result


# Test the one-shot learning classification
test_sentence = "I don't like the food at all."
result = one_shot_classify(test_sentence)
print(f"Classification Result: {result}")
