import re

# Read the file
with open("..\\results\\subExperiments\\resultsQald10turbogpt-4-turbo4.txt", "r", encoding="utf-8") as file:
    file_content = file.read()

# Split queries
queries = file_content.split("QueryNumber:")[1:]

# Function to count triple patterns in a SPARQL query
def count_triple_patterns(sparql_query):
    # Extract the WHERE/ASK clause
    where_clause_match = re.search(r'\{([^}]+)\}', sparql_query, re.DOTALL)
    if not where_clause_match:
        return 0
    
    where_clause = where_clause_match.group(1).strip()
    
    # Remove FILTER and other non-triple patterns
    where_clause = re.sub(r'FILTER\s*\([^)]+\)', '', where_clause)
    
    # Handle OPTIONAL and UNION blocks
    optional_blocks = re.findall(r'OPTIONAL\s*\{([^}]+)\}', where_clause, re.DOTALL)
    union_blocks = re.findall(r'UNION\s*\{([^}]+)\}', where_clause, re.DOTALL)
    
    # Remove OPTIONAL and UNION blocks from the main clause
    where_clause = re.sub(r'OPTIONAL\s*\{[^}]+\}', '', where_clause, flags=re.DOTALL)
    where_clause = re.sub(r'UNION\s*\{[^}]+\}', '', where_clause, flags=re.DOTALL)
    
    # Split into individual triples
    triples = re.split(r'\.\s*', where_clause)
    triples = [t.strip() for t in triples if t.strip()]
    
    # Count triples in OPTIONAL blocks
    for block in optional_blocks:
        block_triples = re.split(r'\.\s*', block)
        block_triples = [t.strip() for t in block_triples if t.strip()]
        triples.extend(block_triples)
    
    # Count triples in UNION blocks
    for block in union_blocks:
        block_triples = re.split(r'\.\s*', block)
        block_triples = [t.strip() for t in block_triples if t.strip()]
        triples.extend(block_triples)
    
    return len(triples)

# Initialize dictionaries to store counts
gold_query_counts = {}  # Total number of gold queries for each pattern type
llm_correct_counts = {}  # Number of correct LLM-generated queries for each pattern type

# Process each query
for query in queries:
    # Extract the correct SPARQL query
    gold_query_match = re.search(r'Correct SPARQL query:\s*(.+?)\s*Generated sparql query:', query, re.DOTALL)
    generated_query_match = re.search(r"Generated sparql query:\s*(.+?)\s*Recall", query, re.DOTALL)
    correctllmquery = re.search(r'Accuracy: 1', query, re.DOTALL)

    if gold_query_match and generated_query_match:
        gold_query = gold_query_match.group(1)
        generated_query = generated_query_match.group(1)

        # Count triple patterns in the gold query
        num_triples = count_triple_patterns(gold_query)
        num_triples_generated_query = count_triple_patterns(generated_query)
        
        # Initialize counts for this pattern type if not already present
        if num_triples not in gold_query_counts:
            gold_query_counts[num_triples] = 0
            llm_correct_counts[num_triples] = 0
        
        # Increment the total number of gold queries for this pattern type
        gold_query_counts[num_triples] += 1
        
        # If the LLM-generated query is correct, increment the correct count
        if num_triples == num_triples_generated_query:
            llm_correct_counts[num_triples] += 1

# Print the results
print("Performance Overview:")
for num_triples in sorted(gold_query_counts.keys()):
    total_gold_queries = gold_query_counts[num_triples]
    correct_llm_queries = llm_correct_counts.get(num_triples, 0)
    print(f"Queries with {num_triples} triples: {total_gold_queries}, {correct_llm_queries}")