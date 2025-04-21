
import torch
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import json
import pickle

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode the sentences from your DataFrame
def find_similar_sentence(query, embeddings, df):
    # Encode the query sentence to get its embedding
    query_embedding = model.encode([query])[0]
    # Compute cosine similarities between the query embedding and all sentence embeddings
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    # Find the index of the sentence with the highest similarity
    closest_index = np.argmax(similarities)
    # Fetch the most similar sentence and its SPARQL query from the DataFrame
    similar_sentence = df.iloc[closest_index]['question']
    sparql_query = df.iloc[closest_index]['query']
    entities = df.iloc[closest_index]['entities']
    relations = df.iloc[closest_index]['relations']
    return similar_sentence, sparql_query,entities,relations


with open('../Datasets/train_lcquad2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract relevant data
rows = []
for item in data:
       # print(question_data)
        question_text_en = item['question']
        query = item['sparql_wikidata']
        relation = item['newPredLabels']
        entities = item['new_LabelsEnt']
        rows.append({"question": question_text_en, "query": query,"entities":entities, "relations":relation})
        

# Create a DataFrame
df_lcquad = pd.DataFrame(rows)
df_lcquad.to_parquet('wikidata_examples.parquet')
embeddings = model.encode(df_lcquad['question'].tolist())

# Save embeddings to a file
with open('embeddings_wikidata.pkl', 'wb') as f:
    pickle.dump(embeddings, f)

# Example query
#query_sentence = "what is the capital of germany?"
#similar_sentence, sparql_query,entities,relations = find_similar_sentence(query_sentence, embeddings, df_lcquad)
#print("Similar Sentence:", similar_sentence)
#print("SPARQL Query:", sparql_query)
#print("entities:", entities)
#print(" relations:", relations)
