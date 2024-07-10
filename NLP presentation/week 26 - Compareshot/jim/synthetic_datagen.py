# Import the necessary modules from the Langchain library
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import random

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="mistral")

# Define a more specific text prompt template
prompt_template = ChatPromptTemplate.from_template("Generate a short phrase or sentence that could be attributed to a {category}. Provide only the text without any additional commentary.")

# Create the chain with model and output parser
chain = prompt_template | llm | StrOutputParser()

# Define categories
categories = ['serial killer', 'non-serial killer']

# Function to generate a single phrase
def generate_phrase(category):
    # Adjust the prompt to include the category dynamically
    response = chain.invoke({"category": category})
    return response

# Generate dataset
data = []
for _ in range(50): # '50' is the total data points that will be generated
    category = random.choice(categories)
    phrase = generate_phrase(category)
    data.append((phrase, category))
    print(f'>>>> Data {_} is created!')

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=['Phrase', 'Category'])
df.to_csv('synthetic_phrases_serial_killer.csv', index=False)

print("Dataset generated successfully!")
