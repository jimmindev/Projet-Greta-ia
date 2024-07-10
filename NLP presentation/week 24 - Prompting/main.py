from transformers import pipeline, set_seed

# Sentiment Analysis

classifier = pipeline("sentiment-analysis")
classifier("I've been waiting for a HuggingFace course my whole life.")

classifier(
    ["I've been waiting for a HuggingFace course my whole life.", "I hate this so much!"]
)

# Text Generation

generator = pipeline("text-generation")
generator("In this course, we will teach you how to")

generator = pipeline("text-generation", model="distilgpt2")
generator(
    "In this course, we will teach you how to",
    max_length=30,
    num_return_sequences=2,
)

unmasker = pipeline("fill-mask")
unmasker("This course will teach you all about <mask> models.", top_k=2)