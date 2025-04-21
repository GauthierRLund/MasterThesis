
import re 
with open("..\\results\\subExperiments\\resultsQald10turbogpt-4-turbo4.txt", "r",  encoding = "utf-8") as file:
    file_content = file.read()


# Regular expression to match prefixes and identifiers based on colons (wd:, wdt:, etc.)
colon_pattern = r'([A-Za-z]+):([A-Za-z0-9]+)\*?'

# Regular expression to match identifiers inside URIs (e.g., /P123 or /Q456)
uri_pattern = r'<http://www.wikidata.org/(entity|prop/direct|prop/statement|prop)/([A-Za-z0-9]+)>'

# Split the content by "QueryNumber" to get each query block
queries = file_content.split("QueryNumber:")

different_keywords_correct_queries = {"FILTER": 0, "ORDER BY ASC": 0, "LIMIT": 0, "ASK": 0, "UNION": 0, "MINUS": 0, "COUNT": 0, "GROUP BY": 0,  "ORDER BY DESC": 0, "YEAR": 0, "OFFSET": 0}
different_keywords_llm_queries = {"FILTER": 0, "ORDER BY ASC": 0, "LIMIT": 0, "ASK": 0, "UNION": 0, "MINUS": 0, "COUNT": 0, "GROUP BY": 0,  "ORDER BY DESC": 0, "YEAR": 0, "OFFSET": 0}
overlap_keywords = {"FILTER": 0, "ORDER BY ASC": 0, "LIMIT": 0, "ASK": 0, "UNION": 0, "MINUS": 0, "COUNT": 0, "GROUP BY": 0,  "ORDER BY DESC": 0, "YEAR": 0, "OFFSET": 0}


prefix_map = {
    'prop/direct': 'wdt:',
    'entity': 'wd:',
    'prop/statement': 'ps:',
    'prop': 'p:'
}

sparql_keywords = ["FILTER", "ORDER BY ASC", "LIMIT", "ASK",  "UNION", "MINUS", "COUNT", "GROUP BY", "ORDER BY DESC", "YEAR"]

# Function to extract SQL-like keywords from queries
def keywords(query, d_kw):
    
    # Tokenize the query and find common SQL-like keywords
    kw = []
    for keyword in sparql_keywords:
        if keyword in query or keyword.lower() in query:
            kw.append(keyword)
            d_kw[keyword] += 1


    return set(kw)
            

def transform_uris(uris):
    transformed_uris = []
    for uri in uris:
        if isinstance(uri, tuple):  # If it's a tuple, apply the transformation
            uri_type, identifier = uri
            if uri_type in prefix_map:
                transformed_uris.append(f"{prefix_map[uri_type]}{identifier}")
        elif isinstance(uri, str):  # If it's already a string, leave it unchanged
            transformed_uris.append(uri)
    return transformed_uris



# Function to extract identifiers from a query block
def extract_identifiers(query):
    # Extract identifiers with the colon pattern (e.g., wd:Q123, wdt:P456)
    colon_identifiers = re.findall(colon_pattern, query)
    # Extract identifiers from URIs (e.g., /P31 or /Q33506)
    uri_identifiers = re.findall(uri_pattern, query)
    identifiers = [prefix + ":" + identifier for prefix, identifier in colon_identifiers] + uri_identifiers
    ids = transform_uris(identifiers)

    
    return ids


def count_shared_keywords(keywords):
    for keyword in keywords:
        overlap_keywords[keyword] += 1 

def compare_ids(correct_identifiers, generated_identifiers):
    dataset_property_ids = set([id_ for id_ in correct_identifiers if "P" in id_.split(":")[1]])
    dataset_item_ids = set([id_ for id_ in correct_identifiers if "Q" in id_.split(":")[1]])

    generated_property_ids = set([id_ for id_ in generated_identifiers if "P" in id_.split(":")[1]])
    generated_item_ids = set([id_ for id_ in generated_identifiers if "Q" in id_.split(":")[1]])

    correct_property_ids = False
    correct_item_ids = False

    print("dataset_property_ids" + str(dataset_property_ids))
    print("generated_property_ids" + str(generated_property_ids))
    print()
    print("dataset_item_ids" + str(dataset_item_ids))
    print("generated_item_ids" + str(generated_item_ids))


    if dataset_property_ids.intersection(generated_property_ids) == dataset_property_ids:
        correct_property_ids = True

    if dataset_item_ids.intersection(generated_item_ids) == dataset_item_ids:
        correct_item_ids = True

    return correct_property_ids, correct_item_ids
def extractPidsAndQids(correct_identifiers):
    dataset_property_ids = [id_ for id_ in correct_identifiers if "P" in id_.split(":")[1]]
    dataset_item_ids = [id_ for id_ in correct_identifiers if "Q" in id_.split(":")[1]]


    return dataset_property_ids, dataset_item_ids

    
    
number_of_queries_correct_ids = 0
number_of_queries_correct_item_ids = 0
number_of_queries_correct_property_ids = 0



# Lists to store query results
comparison_results = []
num_queries_correct_identifiers = 0
a = 0
correctIdentfiers = []
# Iterate through each query block (starting from index 1 because index 0 is the file header)
for query in queries[1:]:
    # Extract the correct SPARQL query
    correct_query_match = re.search(r'Correct SPARQL query:\s*(.+?)\s*Generated sparql query:', query, re.DOTALL)
    generated_query_match = re.search(r"Generated sparql query:\s*(.+?)\s*Recall", query, re.DOTALL)
    correctllmquery = re.search(r'Accuracy: 1', query,re.DOTALL)


    if (correctllmquery):
        number_of_queries_correct_property_ids += 1 
        number_of_queries_correct_item_ids += 1
        number_of_queries_correct_ids += 1
        correct_query = correct_query_match.group(1)
        generated_query = generated_query_match.group(1)
        
        kw_correct_query = keywords(correct_query, different_keywords_correct_queries)
        kw_generated_query = keywords(generated_query, different_keywords_llm_queries)
        shared_keywords = kw_correct_query.intersection(kw_generated_query)
        count_shared_keywords(shared_keywords)
        correct_ids = extract_identifiers(correct_query)

        correctIdentfiers.append(correct_ids)

        pids, qids = extractPidsAndQids(correct_ids)
        generated_ids = extract_identifiers(generated_query)

        comparison_results.append({
            'QueryNumber': queries.index(query),
            'Correct Identifiers': correct_ids,
            'Qids': qids,
            'Pids': pids,
            'Generated Identifiers': generated_ids,
            'Difference': set(correct_ids).symmetric_difference(set(generated_ids))
        })


    else: 
        # Extract identifiers from the correct and generated queries
        correct_query = correct_query_match.group(1)
        generated_query = generated_query_match.group(1)
        a += 1
        print(a)


        kw_correct_query = keywords(correct_query, different_keywords_correct_queries)
        kw_generated_query = keywords(generated_query, different_keywords_llm_queries)
        shared_keywords = kw_correct_query.intersection(kw_generated_query)
        count_shared_keywords(shared_keywords)



        
        
        correct_ids = extract_identifiers(correct_query)
        correctIdentfiers.append(correct_ids)

        generated_ids = extract_identifiers(generated_query)
        
        property_ids, item_ids = compare_ids(correct_ids, generated_ids)
        pids, qids = extractPidsAndQids(correct_ids)

        if property_ids:
            number_of_queries_correct_property_ids += 1 
        if item_ids:
            number_of_queries_correct_item_ids += 1

        if property_ids and item_ids:
            number_of_queries_correct_ids += 1

        

        # Compare the identifiers
        comparison_results.append({
            'QueryNumber': queries.index(query),
            'Correct Identifiers': correct_ids,
            'Qids': qids,
            'Pids': pids,
            'Generated Identifiers': generated_ids,
            'Difference': set(correct_ids).symmetric_difference(set(generated_ids))
        })

'''
with open('correctQidsQald10.txt', 'w') as identifiersQids, open('correctPidsQald10.txt', 'w') as identifiersPids:

# Output the comparison results
    for result in comparison_results:
        print(f"QueryNumber: {result['QueryNumber']}")
        print(f"Correct Identifiers: {result['Correct Identifiers']}")
        identifiersQids.write(f"{result['Qids']}")
        identifiersQids.write("\n")
        identifiersPids.write(f"{result['Pids']}")
        identifiersPids.write("\n")
        

        #print(f"Generated Identifiers: {result['Generated Identifiers']}")
        #print(f"Difference: {result['Difference']}")
        #print("\n")
    '''
print("correct identifiers:" + str(num_queries_correct_identifiers))

print("number_of_queries_correct_property_ids: " + str(number_of_queries_correct_property_ids))
print("number_of_queries_correct_item_ids: " + str(number_of_queries_correct_item_ids))
print("number_of_queries_correct_ids: " + str(number_of_queries_correct_ids))


