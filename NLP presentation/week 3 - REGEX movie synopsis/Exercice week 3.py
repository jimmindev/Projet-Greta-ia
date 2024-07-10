import pandas as pd
import nltk
import string
import re

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


# Download the necessary data
if 'install' == 'noinstall' :
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")

# Load your Excel file
file_path = "movie_synopsis.xlsx"

# Obtain the list of sheet names
excel_sheets = pd.ExcelFile(file_path).sheet_names

# Load data from the first sheet (you can adjust as needed)
excel_data = pd.read_excel(file_path, sheet_name=excel_sheets[0], header=0)

# Assuming the first row contains the column names
column_names = excel_data.iloc[0]
# Set the column names
excel_data.columns = column_names
# Drop the first row as it is now redundant
excel_data = excel_data.iloc[1:]

# Get the text from the 'plot_synopsis' column (change [1] if needed)
text = excel_data['plot_synopsis'].iloc[0]

# Tokenize the text into words
words = word_tokenize(text)



# Extract actors (persons) and locations
actors = []
locations = []


def clean_link(text):
    url_pattern =  re.compile(r"https?://\S+")
    return url_pattern.sub('', text )

def remove_ponctuation(text):
    regular_ponct = list(string.punctuation)
    for ponct in regular_ponct:
        if ponct in text :
            text = text.replace(ponct , ' ' )
    return text

def clean_space(text):
    return text.split()

def remove_stopwords_from_list(liste):
    stop_words = set(stopwords.words("english"))
    word_token = liste
    
    filter_text = [word for word in word_token if word.lower() not in stop_words]
    return filter_text


def stem_words_from_list(liste):
    word_tokens = liste
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems

def lema_words_from_list(liste):
    word_tokens = liste
    lemas = [lemmatizer.lemmatize(word) for word in word_tokens]
    return lemas

def only_start_with_capital(liste):
    word_tokens = liste
    cap_start_strings = [word for word in word_tokens if word and word[0].isupper()]
    return cap_start_strings

def extract_text_inside_parentheses(text):
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

result = extract_text_inside_parentheses(text)
print(result)
exit()


text = clean_link(text)
text = remove_ponctuation(text)
#text = clean_space(text)
 
text = nltk.word_tokenize(text)
text = remove_stopwords_from_list(text)
#text = stem_words_from_list(text)
text = lema_words_from_list(text)

#capital only
text = only_start_with_capital(text)

#for s1 , s2 in zip(text,text):
#    if stem_words_from_list([s2])[0] == s1.lower() :
#        print(s1 + " -> " + stem_words_from_list([s2])[0])

#print(text)

# Print the results
#print("Actors:", actors) 
#print("Locations:", locations)