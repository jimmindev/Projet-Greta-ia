from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

# Initialize the ChatOllama model for Llama3
llm = ChatOllama(model="llama3")

# Zero-Shot Function
def classify_text(text):
    prompt_template = ChatPromptTemplate.from_template(
        "Classify the following text into one of these categories: complaint, compliment, question: '{text}'. Just give me exactly the predicted label without any opening or closing statement from you."
    )
    chain = prompt_template | llm | StrOutputParser()
    result = chain.invoke({'text': text})
    return result

# One shot
def one_shot_classify(text):
    examples = """
    Sentence: 'Your service was excellent!' Classification: compliment
    Sentence: 'Why haven't you responded to my emails?' Classification: question
    Sentence: 'This product is terrible.' Classification: complaint
    """
    prompt_template = ChatPromptTemplate.from_template(
        f"Classify the following sentences into one of these categories: compliment, complaint, question.\n{examples}\nSentence: '{{text}}' Classification: .  Just give me exactly the predicted label without any opening or closing statement from you."
    )
    chain = prompt_template | llm | StrOutputParser()
    result = chain.invoke({'text': text})
    return result

# Few shot
def few_shot_classify(text):
    examples = """
    Sentence: 'Thank you for your outstanding service!' Classification: compliment
    Sentence: 'This is not what I ordered, can you help?' Classification: question
    Sentence: 'I'm not happy with this product at all.' Classification: complaint
    Sentence: 'Can you explain your return policy?' Classification: question
    Sentence: 'I loved the friendly staff!' Classification: compliment
    """
    prompt_template = ChatPromptTemplate.from_template(
        f"Classify the following sentences into one of these categories: compliment, complaint, question.\n{examples}\n Sentence: '{{text}}' Classification: . Just give me exactly the predicted label without any opening or closing statement from you."
    )
    chain = prompt_template | llm | StrOutputParser()
    result = chain.invoke({'text': text})
    return result

#####

# Load the dataset
df = pd.read_csv('/Users/ningrumdaud/GRETA/Ollama/synthetic_customer_chats.csv')

# Apply the classification functions
df['Zero_Shot'] = df['Chat'].apply(classify_text)
df['One_Shot'] = df['Chat'].apply(one_shot_classify)
df['Few_Shot'] = df['Chat'].apply(few_shot_classify)

print(df)
df.to_csv('synthetic_customer_chats.csv', index=False)

# Comparing the performance

def calculate_accuracy(df, column):
    return (df[column] == df['Category']).mean()

zero_shot_accuracy = calculate_accuracy(df, 'Zero_Shot')
one_shot_accuracy = calculate_accuracy(df, 'One_Shot')
few_shot_accuracy = calculate_accuracy(df, 'Few_Shot')

print(f"Zero-Shot Accuracy: {zero_shot_accuracy}")
print(f"One-Shot Accuracy: {one_shot_accuracy}")
print(f"Few-Shot Accuracy: {few_shot_accuracy}")
