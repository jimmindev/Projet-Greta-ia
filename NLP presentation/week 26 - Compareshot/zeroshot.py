from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="llama3")

# Define the zero-shot classification function
def classify_text(text):
    # Define the prompt with an explicit instruction for classification
    prompt_template = ChatPromptTemplate.from_template(
        "Classify the following text into one of these categories: social science, STEM, command: '{text}'. Just give me exactly the predicted label without any opening or closing statement from you."
    )
    
    # Combine the components into a chain
    chain = prompt_template | llm | StrOutputParser()
    
    # Invoke the chain to execute the classification task
    # Here, we pass the text as an input in a dictionary where the key matches the placeholder in the template
    result = chain.invoke({'text': text})
    return result

# Testing the classification function with sample texts
texts = [
    "The findings highlight both the resilience and vulnerability of indigenous cultures in a globalized world.",
    "By analyzing statistical data and theoretical frameworks, we will see how socioeconomic status influences educational attainment and perpetuates inequality.",
    "In this article, we discuss the development of CRISPR-Cas9 as a tool for genome editing.",
    "Utilizing machine learning techniques, our model predicts traffic patterns and dynamically adjusts bandwidth allocations to improve efficiency and reduce latency.",
    "This report analyzes the effectiveness of recent voting reforms in increasing democratic participation."
]

results = {text: classify_text(text) for text in texts}
print(results)
