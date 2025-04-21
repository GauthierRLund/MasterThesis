import re

# Read the file
with open("..\\results\\baselinePerformance\\resultsQald10turbogpt-4-turbo.txt", "r", encoding="utf-8") as file:
    file_content = file.read()

# Split queries
queries = file_content.split("QueryNumber:")[1:]

# Define SPARQL keywords to look for
sparql_keywords = [
    "SELECT", "WHERE", "FILTER", "ORDER BY ASC", "ORDER BY DESC", "LIMIT", "ASK",
    "COUNT", "GROUP BY", "OFFSET", "OPTIONAL", "BIND", "MINUS", "UNION", "YEAR",
]

# Initialize a dictionary to store unique keyword combinations and their counts
keyword_combinations = {}
kw = []
# Function to extract keywords from a query
def extract_keywords(query):
    keywords_found = set()
    for keyword in sparql_keywords:
        if re.search(rf"\b{keyword}\b", query, re.IGNORECASE):
            keywords_found.add(keyword)
    return frozenset(keywords_found)  # Use frozenset for immutability

def extractKeywords(query):
    keywords_found = []
    for keyword in sparql_keywords:
        if re.search(rf"\b{keyword}\b", query, re.IGNORECASE):
            keywords_found.append(keyword)
    return keywords_found  # Use frozenset for immutability

# Process each query
for query in queries:
    # Extract the generated SPARQL query
    correctllmquery = re.search(r'Accuracy: 1', query, re.DOTALL)

    gold_query_match = re.search(r'Correct SPARQL query:\s*(.+?)\s*Generated sparql query:', query, re.DOTALL)
    if gold_query_match:
        generated_query = gold_query_match.group(1)
        # Extract keywords from the query
        keywords = extract_keywords(generated_query)
        k = extractKeywords(generated_query)
        kw.append(k)
        
        # Initialize the keyword combination in the dictionary if not already present
        if keywords not in keyword_combinations:
            keyword_combinations[keywords] = {"total": 0, "correct": 0}
        
        # Increment the total count for this keyword combination
        keyword_combinations[keywords]["total"] += 1
        
        if correctllmquery:
            keyword_combinations[keywords]["correct"] += 1
queries = 0
# Print all unique keyword combinations and their counts
print("Keyword Combinations, Total Queries, and Correct Queries:")
for combination, counts in keyword_combinations.items():
    print(f"{', '.join(combination)}: Total Queries = {counts['total']}, Correct Queries = {counts['correct']}")
print(kw)
