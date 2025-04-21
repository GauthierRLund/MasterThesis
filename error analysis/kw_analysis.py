import re

# Read the file content
with open("..\\results\\subExperiments\\resultsQald10turbogpt-4-turbo4.txt", "r", encoding="utf-8") as file:
    file_content = file.read()

# Split the content into individual queries
queries = file_content.split("QueryNumber:")

# List of SPARQL keywords to analyze
sparql_keywords = ["FILTER", "ORDER BY ASC", "LIMIT", "ASK", "UNION", "MINUS", "COUNT", "GROUP BY", "ORDER BY DESC", "YEAR", "OFFSET", "OPTIONAL", "BIND"]

# Initialize dictionaries to store counts
count_keywords_gold_queries = {keyword: 0 for keyword in sparql_keywords}
count_keywords_llm_queries = {keyword: 0 for keyword in sparql_keywords}
overlap_keywords = {keyword: 0 for keyword in sparql_keywords}

# Initialize dictionaries to store TP, TN, FP, FN for each keyword
true_positives = {keyword: 0 for keyword in sparql_keywords}
true_negatives = {keyword: 0 for keyword in sparql_keywords}
false_positives = {keyword: 0 for keyword in sparql_keywords}
false_negatives = {keyword: 0 for keyword in sparql_keywords}

# Function to extract SPARQL keywords from queries
def extract_sparql_keywords(query, d_kw):
    kw = []
    for keyword in sparql_keywords:
        if keyword in query or keyword.lower() in query:
            kw.append(keyword)
            d_kw[keyword] += 1
    return set(kw)

# Function to count overlapping keywords
def count_overlapping_keywords(keywords):
    for keyword in keywords:
        overlap_keywords[keyword] += 1

# Function to update TP, TN, FP, FN for each keyword
def update_confusion_matrix(gold_keywords, generated_keywords):
    for keyword in sparql_keywords:
        if keyword in gold_keywords and keyword in generated_keywords:
            true_positives[keyword] += 1
        elif keyword not in gold_keywords and keyword not in generated_keywords:
            true_negatives[keyword] += 1
        elif keyword not in gold_keywords and keyword in generated_keywords:
            false_positives[keyword] += 1
        elif keyword in gold_keywords and keyword not in generated_keywords:
            false_negatives[keyword] += 1

# Process each query
for query in queries[1:]:
    # Extract the correct SPARQL query
    gold_query_match = re.search(r'Correct SPARQL query:\s*(.+?)\s*Generated sparql query:', query, re.DOTALL)
    generated_query_match = re.search(r"Generated sparql query:\s*(.+?)\s*Recall", query, re.DOTALL)
    correctllmquery = re.search(r'Accuracy: 1', query, re.DOTALL)

    if gold_query_match and generated_query_match:
        gold_query = gold_query_match.group(1)
        generated_query = generated_query_match.group(1)

        # Extract keywords from gold and generated queries
        kw_correct_query = extract_sparql_keywords(gold_query, count_keywords_gold_queries)
        kw_generated_query = extract_sparql_keywords(generated_query, count_keywords_llm_queries)

        # Count overlapping keywords
        shared_keywords = kw_correct_query.intersection(kw_generated_query)
        count_overlapping_keywords(shared_keywords)

        # Update confusion matrix for each keyword
        update_confusion_matrix(kw_correct_query, kw_generated_query)

# Print results
print("Gold Query Keyword Counts:", count_keywords_gold_queries)
print("LLM Query Keyword Counts:", count_keywords_llm_queries)
print("Overlapping Keyword Counts:", overlap_keywords)
print("True Positives:", true_positives)
print("True Negatives:", true_negatives)
print("False Positives:", false_positives)
print("False Negatives:", false_negatives)