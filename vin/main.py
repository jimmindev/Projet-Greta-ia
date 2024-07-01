from llama_cpp import Llama
import psycopg2

# Chargez le modèle
llm = Llama(model_path="./mistral-7b-instruct-v0.1.Q5_K_S.gguf")

# Définissez la fonction pour convertir une phrase en langage naturel en requête SQL
def convert_to_sql(input_text):
    # Ajoutez une instruction spécifique pour générer la requête SQL
    input_text = "Convert the following natural language query into a SQL query: " + input_text

    # Générez la requête SQL
    output = llm(input_text, max_tokens=100)

    # Extrayez la requête SQL de la sortie
    sql_query = output["choices"][0]["text"].strip().split("\n")[-1]
    
    print(sql_query)

    return sql_query

# Connectez-vous à la base de données
conn = psycopg2.connect(
    host="192.168.207.128",
    database="jimmy",
    user="jimmy",
    password="Ey4@WKIF!3lm)e*y"
)

# Créez un curseur
cur = conn.cursor()

# Testez la fonction de conversion
input_text = "What is the name of the client who placed order 123?"
sql_query = convert_to_sql(input_text)

# Exécutez la requête SQL
#cur.execute(sql_query)

# Récupérez les résultats
results = cur.fetchall()

# Générez une réponse à partir des résultats
response = "The name of the client who placed order 123 is " + results[0][0]

# Fermez la connexion à la base de données
cur.close()
conn.close()

# Affichez la réponse
print(response)
