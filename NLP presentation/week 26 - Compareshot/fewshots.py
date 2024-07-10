from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="mistral")

def few_shot_classify(text):
    # Examples included in the prompt to teach the model what is expected
    examples = """
    Sentence: 'I am thrilled to be part of this!' Classification: Happiness
    Sentence: 'It has been a tough day.' Classification: Sadness
    Sentence: 'This is a regular, uneventful day.' Classification: Neutral
    """
    prompt_template = ChatPromptTemplate.from_template(
        f"Classify the following sentences into one of these categories: Happiness, Sadness, Neutral.\n{examples}\n Sentence: '{{text}}' Classification: . Just give me the output with dictionary stucture consisting text and predicted label without any opening and closing statement from you."
    )
    
    # Combine the components into a chain
    chain = prompt_template | llm | StrOutputParser()
    
    # Invoke the chain to classify the new text
    result = chain.invoke({'text': text})
    return result

# Test the few-shot learning classification
test_sentence = "I just received my exam results! I am sooooo relief!"
result = few_shot_classify(test_sentence)
print(f"{result}")
