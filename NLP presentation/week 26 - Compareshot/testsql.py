from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="llama3")

# Define the function to convert text to SQL query
def convert_texttosql(text, schema):
    # Define the prompt with an explicit instruction for conversion
    prompt_template = ChatPromptTemplate.from_template(
        f"Convert the following text into SQL formula by considering the SQL schema, command: '{{text}}', schema: '{{schema}}'. Just give me exactly the output consisting text and the SQL formula without any opening or closing statement from you like 'Here is the SQL formula to calculate....'"
    )
    
    # Combine the components into a chain
    chain = prompt_template | llm | StrOutputParser()
    
    # Invoke the chain to execute the conversion task
    # Here, we pass both the text and the schema as inputs in a dictionary where the keys match the placeholders in the template
    result = chain.invoke({'text': text, 'schema': schema})
    return result

# Define the SQL schema
schema = """Tables and their relevant fields:
- Product (ProductID, ProductName)
- LineItem (ProductID, TotalPrice)
- SalesOrder (SalesOrderID, OrderDate)"""

# Testing the function with sample texts
texts = [
    "Calculate the sales in October 2023",
    "Calculate the top 10 products that contribute to the sales"
]

# Create a dictionary with results from the conversion function
results = {text: convert_texttosql(text, schema) for text in texts}
print(results)
