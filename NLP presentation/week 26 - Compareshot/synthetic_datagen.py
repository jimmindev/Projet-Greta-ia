from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import random

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="llama3")

# Define a simple text prompt template
prompt_template = ChatPromptTemplate.from_template("Create a chat or text from customer that is a {category}. Just give me exactly the string text sample without any opening or closing statement from you.")

# Create the chain with model and output parser
chain = prompt_template | llm | StrOutputParser()

# Define categories
categories = ['complaint', 'compliment', 'question']

# Function to generate a single chat
def generate_chat(category):
    # Adjust the prompt to include the category dynamically
    response = chain.invoke({"category": category})
    return response

# Generate dataset
data = []
for _ in range(50): # '50' is the total data points that will be generated
    category = random.choice(categories)
    chat = generate_chat(category)
    data.append((chat, category))
    print(f'>>>> Data {_} is created!')

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=['Chat', 'Category'])
df.to_csv('synthetic_customer_chats.csv', index=False)

print("Dataset generated successfully!")
