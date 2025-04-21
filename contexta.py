import spacy
import spacy_component
import requests

from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
import requests
from refined.inference.processor import Refined


refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikipedia")


#nlp = spacy.load('en_core_web_lg')

#if 'entityfishing' not in nlp.pipe_names:
    #nlp.add_pipe('entityfishing', last=True)  

def entity_linking(question):
    spans = refined.process_text(question)
    data = spans
    entity_ids = []
    # Initialize dictionaries to store results
    for d in data:
        if d.predicted_entity is not None:
            entity_id = d.predicted_entity.wikipedia_entity_title
            entity_label = d.predicted_entity.wikidata_entity_id
            if entity_id is not None:
                entity_ids.append(entity_id + ': ' + entity_label)
    return entity_ids


def relation_extraction(question):
    """This function takes NL question and KB and returns the relations found in the question"""
    rel_list = []

    nlp = spacy.load('en_core_web_lg')
    nlp.add_pipe("rebel", after="senter", config={'device':-1, 'model_name':'Babelscape/rebel-large'})
    doc = nlp(question)
    for value, rel_dict in doc._.rel.items():
        relation =  str(execute_sparql_query(rel_dict['relation']))
        rel_list.append(relation)
    return rel_list
        
        

def execute_sparql_query(label):
    """This function takes label generated from REBEL and return its wikidata identfier"""
    #label = f'"{label}"'
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql_query = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?item ?itemLabel 
            WHERE 
            {
              ?item rdfs:label """+label+"""@en.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }limit 1
            """

    headers = {"Accept": "application/json"}
    response = requests.get(endpoint_url, params={"query": sparql_query}, headers=headers)
    print(f"Response Text: {response.text}")  # Check what the server is actually returning
    data = response.json()
    results = data['results']['bindings']
    item = ""
    for result in results:
        item = result['propertyLabel']['value']
    
    return item

def run_sparql_query(label):
    # Set up the SPARQL endpoint (Wikidata)
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql_query = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?item ?itemLabel 
            WHERE 
            {
              ?item rdfs:label "capital"@en.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }limit 1 
            
            """
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    
    # Query Wikidata and return the results
    try:

        results = sparql.query().convert()
        results = results['results']['bindings']
        item = ""
        for result in results:
            item = result['item']['value']
    
        return item
    
    except (SPARQLExceptions.SPARQLWrapperException, Exception) as e:
        print(e)
        # Return 0 if there's an issue with the query (e.g., invalid SPARQL)
        return "Incorrect query"
    
    


