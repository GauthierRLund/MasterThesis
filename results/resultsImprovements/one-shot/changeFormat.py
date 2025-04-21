import json

# Function to add prefixes to a SPARQL query
def add_prefixes_to_sparql(query):
    # Define the prefixes to add
    prefixes = """

    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX dct: <http://purl.org/dc/terms/> 
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    PREFIX psn: <http://www.wikidata.org/prop/statement/value-normalized/> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX wds: <http://www.wikidata.org/entity/statement/> 
    PREFIX wdv: <http://www.wikidata.org/value/> 
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """


    query = prefixes + query

    return query.strip()  # Remove any leading/trailing whitespace

# Load the file
file_path = "resultsQald10turbogpt-4-turbo.json"  # Replace with your file path
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Iterate through the data and update SPARQL queries
for question in data["questions"]:
    if "query" in question and "sparql" in question["query"]:
        question["query"]["sparql"] = add_prefixes_to_sparql(question["query"]["sparql"])
outFile = "newExperiment-4-Turbo.json"
# Save the updated data back to the file
with open(outFile, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("File updated and saved successfully.")