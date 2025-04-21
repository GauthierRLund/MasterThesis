from sentence_transformers import SentenceTransformer, util
import os
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def example_generation(question, n_similar_queries):
    """
    Generates examples of similar queries based on the input question.

    Args:
        question (str): The input natural language question.
        n_similar_queries (int): The number of similar queries to retrieve.

    Returns:
        str: A formatted string containing the most similar questions, entities, relations, and SPARQL queries.
    """
    # Load pre-computed embeddings and the dataframe
    with open('data/embeddings_wikidata.pkl', 'rb') as f:
        embeddings = pickle.load(f)
    df = pd.read_parquet('data/wikidata_examples.parquet')
    
    # Find the most similar queries
    similar_queries = find_similar_query(question, embeddings, df, n_similar_queries)
    
    # Format the results into a string
    examples = []
    for i, (ques, query, entities, relations) in enumerate(similar_queries, start=1):
        example = f"Example {i}:\n[Question]: {ques} \n[Entities]: {str(entities)}\n[Relations]: {str(relations)} \n[SPARQL]: {query}\n"
        examples.append(example)
    
    return "\n".join(examples)

def find_similar_query(query, embeddings, df, n_similar_queries):
    """
    Finds the most similar queries to the input question.

    Args:
        query (str): The input natural language question.
        embeddings (np.array): Pre-computed embeddings for all questions in the dataframe.
        df (pd.DataFrame): The dataframe containing questions, SPARQL queries, entities, and relations.
        n_similar_queries (int): The number of similar queries to retrieve.

    Returns:
        list: A list of tuples, where each tuple contains:
              - similar_sentence (str): The similar question.
              - sparql_query (str): The corresponding SPARQL query.
              - entities (list): The entities in the question.
              - relations (list): The relations in the question.
    """
    # Encode the input query
    query_embedding = model.encode([query])[0]
    
    # Compute cosine similarities between the input query and all embeddings
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    
    # Get the indices of the top-k most similar queries
    closest_indices = np.argsort(similarities)[-n_similar_queries:][::-1]
    
    # Retrieve the top-k most similar queries and their associated data
    results = []
    for idx in closest_indices:
        similar_sentence = df.iloc[idx]['question']
        sparql_query = df.iloc[idx]['query']
        entities = df.iloc[idx]['entities']
        relations = df.iloc[idx]['relations']
        results.append((similar_sentence, sparql_query, entities, relations))
    
    return results

