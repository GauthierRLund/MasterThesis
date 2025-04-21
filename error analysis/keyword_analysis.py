
import re 
with open("..\\results\\resultsImprovements\\fewshot-5\\resultsQald10turbogpt-4-turbo.txt", "r",  encoding = "utf-8") as file:
    file_content = file.read()


queries = file_content.split("QueryNumber:")

sparql_keywords = ["FILTER", "ORDER BY ASC", "LIMIT", "ASK",  "UNION", "MINUS", "COUNT", "GROUP BY", "ORDER BY DESC", "YEAR", "OFFSET", "OPTIONAL", "BIND"]

count_keywords_gold_queries = {"FILTER": 0, "ORDER BY ASC": 0, "LIMIT": 0, "ASK": 0, "UNION": 0, "MINUS": 0, "COUNT": 0, "GROUP BY": 0,  "ORDER BY DESC": 0, "YEAR": 0, "OFFSET": 0, "OPTIONAL": 0, "BIND": 0}
count_keywords_llm_queries = {"FILTER": 0, "ORDER BY ASC": 0, "LIMIT": 0, "ASK": 0, "UNION": 0, "MINUS": 0, "COUNT": 0, "GROUP BY": 0,  "ORDER BY DESC": 0, "YEAR": 0, "OFFSET": 0, "OPTIONAL": 0, "BIND": 0}
overlap_keywords = {"FILTER": 0, "ORDER BY ASC": 0, "LIMIT": 0, "ASK": 0, "UNION": 0, "MINUS": 0, "COUNT": 0, "GROUP BY": 0,  "ORDER BY DESC": 0, "YEAR": 0, "OFFSET": 0, "OPTIONAL": 0, "BIND": 0}


#Function to extract SPARQL keywords from queries
def extract_sparql_keywords(query, d_kw):
    kw = []
    for keyword in sparql_keywords:
        if keyword in query or keyword.lower() in query:
            kw.append(keyword)
            d_kw[keyword] += 1


    return set(kw)
            
def count_overlapping_keywords(keywords):
    for keyword in keywords:
        overlap_keywords[keyword] += 1 

for query in queries[1:]:
    # Extract the correct SPARQL query
    gold_query_match = re.search(r'Correct SPARQL query:\s*(.+?)\s*Generated sparql query:', query, re.DOTALL)
    generated_query_match = re.search(r"Generated sparql query:\s*(.+?)\s*Recall", query, re.DOTALL)
    correctllmquery = re.search(r'Accuracy: 1', query,re.DOTALL)

    if (correctllmquery):
        continue

    #Comparing LLM generated SPARQL keywords with keywords of gold queries of incorrect LLM generated SPARQL queries 
    else: 
        gold_query = gold_query_match.group(1)
        generated_query = generated_query_match.group(1)


        kw_correct_query = extract_sparql_keywords(gold_query, count_keywords_gold_queries)
        kw_generated_query = extract_sparql_keywords(generated_query, count_keywords_llm_queries)
        shared_keywords = kw_correct_query.intersection(kw_generated_query)
        count_overlapping_keywords(shared_keywords)
        


print(count_keywords_gold_queries)
print(count_keywords_llm_queries)
print(overlap_keywords)
