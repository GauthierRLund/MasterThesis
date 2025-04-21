

import requests
from openai import OpenAI
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
import requests
import time
import rag as r
import json
from transformers import pipeline
import requests
from refined.inference.processor import Refined
import requests

client = OpenAI(api_key= 'API_key')


# Set your OpenAI API key
refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikipedia")
p = [1, 2, 3, 2, 3, 1, 2, 5, 1, 1, 2, 3, 1, 4, 4, 4, 2, 1, 4, 2, 1, 4, 3, 3, 2, 2, 1, 1, 1, 1, 3, 7, 7, 
1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 4, 1, 1, 2, 4, 4, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 
2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 3, 3, 1, 1, 3, 2, 2, 1, 1, 
1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 3, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 3, 1, 2, 1, 1, 2, 2, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 5, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 3, 2, 1, 2, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 
1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 3, 1, 1, 2, 3, 1, 1, 1, 2, 2, 2, 3, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 3, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 2, 
1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1]


k = [['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['ASK'], ['SELECT', 'WHERE'], ['SELECT'], 
['SELECT'], ['SELECT'], ['ASK'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT', 'YEAR'], ['FILTER', 'ASK'], ['SELECT', 'WHERE', 'FILTER', 'ASK', 'COUNT'], ['ASK'], ['FILTER', 'ASK'], ['FILTER', 'ASK'], ['ASK'], ['FILTER', 'ASK'], ['SELECT', 'WHERE', 'FILTER', 'ASK', 'COUNT', 'MINUS'], ['SELECT', 'WHERE', 'COUNT', 'GROUP BY', 'OPTIONAL'], ['ASK'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT', 'COUNT', 'GROUP BY', 'OFFSET'], ['ASK'], ['ASK'], ['FILTER', 'ASK', 'UNION'], ['FILTER', 'ASK', 'YEAR'], ['FILTER', 'ASK', 'YEAR'], ['ASK'], ['ASK'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 
'WHERE', 'COUNT'], ['ASK'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT', 'MINUS'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT', 'YEAR'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT', 'YEAR'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['ASK'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['FILTER', 'ASK'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'ORDER BY DESC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'FILTER', 'COUNT'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT', 'OFFSET', 'BIND', 'YEAR'], ['FILTER', 'ASK', 'YEAR'], ['FILTER', 'ASK'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['FILTER', 
'ASK', 'YEAR'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY ASC', 'LIMIT', 'BIND'], ['FILTER', 'ASK'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'BIND', 'YEAR'], ['SELECT', 'WHERE', 'BIND', 'YEAR'], ['ASK'], ['ASK'], ['ASK'], ['ASK'], ['ASK'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'FILTER', 'ORDER BY ASC', 'LIMIT', 'ASK'], ['FILTER', 'ASK'], 
['SELECT', 'WHERE', 'FILTER', 'ASK', 'COUNT'], ['FILTER', 'ASK'], ['ASK'], ['ASK'], ['ASK'], ['FILTER', 'ASK'], ['FILTER', 'ASK'], ['FILTER', 'ASK'], ['ASK'], ['ASK'], ['ASK'], ['SELECT', 'WHERE', 'FILTER', 'COUNT', 'UNION', 'YEAR'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 
'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'BIND', 'YEAR'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'BIND', 'YEAR'], 
['SELECT', 'WHERE', 'BIND', 'YEAR'], ['ASK'], ['FILTER', 'ASK', 'YEAR'], ['FILTER', 'ASK'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY ASC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['ASK'], ['FILTER', 'ASK'], ['ASK'], ['SELECT', 'WHERE', 'FILTER'], ['ASK'], ['FILTER', 'ASK', 'YEAR'], ['ASK'], ['FILTER', 'ASK', 'YEAR'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'UNION'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'FILTER', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'FILTER', 'ORDER BY DESC', 'LIMIT', 'YEAR'], 
['FILTER', 'ASK'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 
'FILTER', 'ORDER BY DESC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['ASK'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY ASC', 'LIMIT', 'OFFSET'], ['SELECT', 'WHERE', 'FILTER', 'YEAR'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER', 'YEAR'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['FILTER', 'ASK'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 
'WHERE', 'FILTER', 'COUNT', 'YEAR'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER', 'COUNT', 'YEAR'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'BIND', 'YEAR'], ['SELECT', 'WHERE', 'BIND', 'YEAR'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 
'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY ASC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY ASC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['FILTER', 'ASK'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 
'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER', 'BIND'], ['SELECT', 'WHERE', 'COUNT', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['FILTER', 'ASK', 'BIND', 'YEAR'], ['SELECT', 'WHERE'], ['SELECT', 
'WHERE', 'COUNT', 'BIND'], ['ASK'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER', 'ORDER BY ASC', 'LIMIT'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT', 'COUNT', 'GROUP BY'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 
'FILTER', 'YEAR'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['ASK'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'UNION'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT'], ['SELECT', 'WHERE', 'ORDER BY ASC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'UNION'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'FILTER', 'ORDER BY ASC', 'LIMIT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'ORDER BY DESC', 'LIMIT'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'COUNT', 'BIND'], ['ASK', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE', 'BIND'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE', 'COUNT'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE'], ['SELECT', 'WHERE']]

prefixes = """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
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
def refinedEntityLinker(nlQuestion):

    spans = refined.process_text(nlQuestion)
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

def get_sparql_from_chatgpt(prompt, gpt_model):
    print("\n")
    print("Generated_prompt")
    print(prompt)
    response = client.chat.completions.create(
                model=gpt_model,
                messages=[{"role": "user", "content": prompt}]
            )
    return response.choices[0].message.content


def formate_output(response):
    sparql_query = ""
    if '```' in response:
        sparql_query = response.split('```')[1]
        if 'sparql' in sparql_query:
            sparql_query = sparql_query.split('sparql')[1]
            return sparql_query
        if 'SPARQL' in sparql_query:
            sparql_query = sparql_query.split('SPARQL')[1]
        return sparql_query
    if '[sparql]:' in response:
        return response.split('[sparql]:')[1]
    if '[SPARQL]:' in response:
        return response.split('[SPARQL]:')[1]
    else:
        return response



def run_sparql_query(query):

    prefixes_query = prefixes + query
    # Set up the SPARQL endpoint (Wikidata)
    sparql = SPARQLWrapper("https://skynet.coypu.org/wikidata/")
    sparql.setQuery(prefixes_query)
    sparql.setReturnFormat(JSON)
    
    # Query Wikidata and return the results
    sparql.setTimeout(300)

    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Incorrect query"

def generateSetResults(generated_results, correct_results):
    if generated_results != 0:
        if generated_results.get('boolean') == False:
            generated_set = 'false'
        elif generated_results.get('boolean') == True:
            generated_set = 'true'
        else:
            vars_list = generated_results.get('head', {}).get('vars', [])
            if not vars_list:
                print("No variables returned in the query.")
                generated_set = set()
            
            else:

                variable_name = vars_list[0]  # Safe to access first item since we've checked
                generated_bindings = generated_results.get('results', {}).get('bindings', [])
                generated_set = set(
                result[variable_name]['value'] for result in generated_bindings if variable_name in result
        ) 
    else: 
        generated_set = set()


    if correct_results != 0:
        if correct_results.get('boolean') == False:
            correct_set = 'false'
        elif correct_results.get('boolean') == True:
            correct_set = 'true'
        else:
            variable_name_correct_results = correct_results.get('head', {}).get('vars', [None])[0]
            generated_bindings_correct_results = correct_results.get('results', {}).get('bindings', [])
            correct_set = set(
            result[variable_name_correct_results]['value'] for result in generated_bindings_correct_results if variable_name_correct_results in result
        )   
    else:
        correct_set = set()

    return correct_set, generated_set

def calculateMetrics(llmResults, correctResults):        
        intersection = llmResults.intersection(correctResults)

        # Precision: relevant retrieved results / all retrieved results
        precision = len(intersection) / len(llmResults) if llmResults else 0
        
        # Recall: relevant retrieved results / all relevant results
        recall = len(intersection) / len(correctResults) if correctResults else 0
        
        # Accuracy: 1 if both result sets are identical, else 0
        #Accuracy is 1 if llm generates correct query that returns labels
        accuracy = 1 if llmResults == correctResults else 0
 
        return precision, recall, accuracy

def writingToFile(file, queryNumber, nlQuestion, generatedSparqlQuery, sparqlQueryDataset, incorrectQueryLLm = False, incorrectQueryDataset = False, precision = 0, recall = 0, accuracy = 0):

        file.write('QueryNumber: ' + str(queryNumber) + 
                    '\n Natural language question: ' + str(nlQuestion) +
                    '\n Correct SPARQL query: \n' + str(sparqlQueryDataset) +
                    '\n Generated sparql query: \n' + str(generatedSparqlQuery) +
                    '\n Recall: ' + str(recall) +
                    '\n Accuracy: ' + str(accuracy) + 
                    '\n Precision: ' + str(precision) +
                    '\n Query error LLM: ' + str(incorrectQueryLLm) + 
                    '\n Query error dataset: ' + str(incorrectQueryDataset))
        
        file.write('\n')
        file.write('\n')    

def prompt_building(question, entities, relations, instruction, experiment, query_number):
    """This function return a final prompt that will include everyting and LLM ready"""
    
    
    if experiment == 1:
        prompt = instruction +  "\n[question]:" + question + "\nEntities :"+ str(entities) + question + "\nRelations :"+ str(relations) 
    
    
    if experiment == 2:
        prompt = instruction +  "\n[question]:" + question + "\nEntities :"+ str(entities) + question + "\nRelations :"+ str(relations) + "\nNumber of patterns :" + str(p[query_number])
    

    if experiment == 3:
        prompt = instruction +  "\n[question]:" + question + "\nEntities :"+ str(entities) + question + "\nRelations :"+ str(relations) + "\nKeywords :" + str(k[query_number])
    
    
    if experiment == 4:
        prompt = instruction +  "\n[question]:" + question + "\nEntities :"+ str(entities) + question + "\nRelations :"+ str(relations) + "\nNumber of patterns :" + str(p[query_number]) + "\nKeywords :" + str(k[query_number])
    
    
        
    
    return prompt




# Main function to handle translation and comparison
def main(gptmodel, instruction, experiment):
    gpt = gptmodel.replace(":", "_")
    file = open(("resultsQald10turbo" + gpt + str(experiment) + ".txt"), 'w', encoding='utf-8')
    number_of_queries = 0
    a = 0
    p = 0
    r = 0

    incorrect_queries_dataset = 0
    incorrect_queries_llm = 0
    with open("Datasets/test_qald_10.json", 'r', encoding='utf-8') as dataset_file, open("error analysis/correctPidsQald10.txt", 'r', encoding='utf-8') as pids_relations, open("error analysis/correctQidsQald10.txt", 'r', encoding='utf-8') as qids_entities:
        qald10Test = json.load(dataset_file)
        output_data = {
        "dataset": {
            "id": "qald-X"
        },
        "questions": []
    }
        relations = [line.strip() for line in pids_relations]
        entities = [line.strip() for line in qids_entities]

        counter = 0
        for question, rel, e in zip(qald10Test["questions"], relations, entities):
            sparql_query = question.get("query", {}).get("sparql", "")
            counter += 1 
            for q in question["question"]:
                if q["language"] == "en":
                    nl_question = q["string"]
                    break
            prompt = prompt_building(nl_question, e, rel, instruction, experiment, number_of_queries)

            generated_sparql_query = get_sparql_from_chatgpt(prompt, gptmodel)

            print(generated_sparql_query)
            llm_sparql_query = formate_output(generated_sparql_query)
            results_from_llm_query = run_sparql_query(llm_sparql_query)

            retries = 0
            while retries < 3 and results_from_llm_query == "Incorrect query":
                
                # Regenerate the SPARQL query using GPT
                generated_sparql_query = get_sparql_from_chatgpt(prompt, gptmodel)
                llm_sparql_query = formate_output(generated_sparql_query)
                
                # Rerun the SPARQL query
                results_from_llm_query = run_sparql_query(llm_sparql_query)
                
                retries += 1

            correct_results = run_sparql_query(sparql_query)
            expected_sparql_query = sparql_query



            number_of_queries += 1
            prefixes_sparql_query = prefixes + llm_sparql_query

            question_entry = {
                "id": question.get("id", 0),
                "aggregation": question.get("aggregation", False),
                "question": [
                    {"language": "en", "string": nl_question}
                ],
                "answers": [results_from_llm_query],
                "query": {"sparql": prefixes_sparql_query}
            }


            output_data["questions"].append(question_entry)
        


   
            if correct_results == "Incorrect query" and results_from_llm_query == "Incorrect query":
                incorrect_queries_dataset += 1
                incorrect_queries_llm += 1
                writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, incorrectQueryLLm=True, incorrectQueryDataset=True)
                continue



            if correct_results == "Incorrect query":
                print("incorrect query dataset" + str(number_of_queries))
                incorrect_queries_dataset += 1
                writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, incorrectQueryDataset=True)
                continue


            if results_from_llm_query == "Incorrect query":
                incorrect_queries_llm += 1
                writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, incorrectQueryLLm=True)
                continue


            setCorrectResults, setLLMResults = generateSetResults(results_from_llm_query, correct_results)
         
            if not setCorrectResults:
                print("empty query dataset" + str(number_of_queries) + str(setCorrectResults))
            if 'boolean' in results_from_llm_query and 'boolean' in correct_results:
                if results_from_llm_query == correct_results:
                    writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, accuracy=1, precision=1, recall=1)
                    p += 1
                    r += 1
                    a += 1
                else: 
                    writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, accuracy=0, precision=0, recall=0)


            elif not (setCorrectResults or setLLMResults):
                writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, accuracy=1, precision=1, recall=1)
                p += 1
                r += 1
                a += 1

            
            elif 'boolean' in results_from_llm_query or 'boolean' in correct_results:
                writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, accuracy=0, precision=0, recall=0)

            else:
                precision, recall, accuracy = calculateMetrics(setLLMResults, setCorrectResults)
                p += precision
                r += recall
                a += accuracy
                writingToFile(file, number_of_queries, nl_question, generated_sparql_query, expected_sparql_query, accuracy=accuracy, precision=precision, recall=recall)


        file.write("number of incorrect llm generated queries: " + str(incorrect_queries_llm) + 
                   "\nnumber of incorrect llm generated queries: " + str(incorrect_queries_llm) +
                   "\nnumber of incorrect queries from dataset: " + str(incorrect_queries_dataset) +
                   "\nPrecision: " + str(p) +
                   "\naccuracy: " + str(a) + 
                   "\nrecall: " + str(r))

                
        file.write('\n')
        file.write('\n')  

        with open("resultsQald10turbo" + gpt + str(experiment) +".json", "w", encoding="utf-8") as output_json_file:
            json.dump(output_data, output_json_file, indent=4, ensure_ascii=False)

            

if __name__ == "__main__":
    instruction = """[INST]
        Task: Convert question to SPARQL query for wikidata knowledge graph. Only generate the SPARQL query nothing else. \n
        Description: Given an input question, along with a list of QIDs and PIDs corresponding to the entities and relations in the question, generate a correct SPARQL query.
                [/INST] \n
    """
    main("gpt-4-turbo", instruction, 1)
    instruction = """[INST]
        Task: Convert question to SPARQL query for wikidata knowledge graph. Only generate the SPARQL query nothing else. \n
        Description: Given an input question, along with a list of QIDs and PIDs corresponding to the entities and relations in the question, the number of patterns in the query, generate a correct SPARQL query.
                [/INST] \n
    """
    main("gpt-4-turbo", instruction, 2)

    instruction = """[INST]
        Task: Convert question to SPARQL query for wikidata knowledge graph. Only generate the SPARQL query nothing else. \n
        Description: Given an input question, along with a list of QIDs and PIDs corresponding to the entities and relations in the question, and a set of keywords required for the query, generate a correct SPARQL query.
                [/INST] \n
    """
    main("gpt-4-turbo", instruction, 3)
    
    instruction = """[INST]
        Task: Convert question to SPARQL query for wikidata knowledge graph. Only generate the SPARQL query nothing else. \n
        Description: Given an input question, a list of QIDs and PIDs corresponding to the entities and relations in the question, the required number of patterns, and a set of keywords to be included in the query, generate a correct SPARQL query.
                [/INST] \n
    """
    main("gpt-4-turbo", instruction, 4)
    


