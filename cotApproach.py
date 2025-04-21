

import requests
from openai import OpenAI
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
import requests
import time
import contextb as cb
import contexta as ca
import json




# Set your OpenAI API key
client = OpenAI(api_key= 'API_key')

import requests
from refined.inference.processor import Refined




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

# Function to get SPARQL query from ChatGPT for a given NL question
def get_sparql_from_gpt(prompt, gpt_model):
    print("\n")
    print("Generated_prompt")
    print(prompt)
    response = client.chat.completions.create(
                model=gpt_model,
                messages=[{"role": "user", "content": prompt}]
            )
    return response.choices[0].message.content

def run_sparql_query(query):


    prefixes_query = prefixes + query
    # Set up the SPARQL endpoint (Wikidata)
    sparql = SPARQLWrapper("https://skynet.coypu.org/wikidata/")
    sparql.setQuery(prefixes_query)
    sparql.setReturnFormat(JSON)
    
    # Query Wikidata and return the results
    try:

        results = sparql.query().convert()
        return results
    
    except (SPARQLExceptions.SPARQLWrapperException, Exception) as e:
        print(e)
        # Return 0 if there's an issue with the query (e.g., invalid SPARQL)
        return "Incorrect query"

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

def prompt_building(question, relations):
    """This function return a final prompt that will include everyting and LLM ready"""
    
    instruction = """[INST]
        Task: Convert question to SPARQL query for wikidata knowledge graph.\n
        Description: Given an input question and a list of wikidata URIs for the mentioned entities in the question and relations 
        mentioned in the question. Write a correct SPARQL code to query these wikidata URIs in the wikidata Knowledge graph. 
                [/INST] \n
"""
   # print(instruction)
    prompt = instruction + "You can formulate your SPARQL query as the following SPARQL example. \n" + str(cb.example_generation(question, 1)) +"\n[question]:"+ question + "\n[Entities] :"+ str(ca.entity_linking(question)) + "\n[Relations]:" + str(relations) + "\nLet's think step by step"
    return prompt
    





# Main function to handle translation and comparison
def main(gptmodel):
    gpt = gptmodel.replace(":", "_")
    file = open(("results" + gpt +".txt"), 'w', encoding='utf-8')

    number_of_queries = 0
    a = 0
    p = 0
    r = 0

    incorrect_queries_dataset = 0
    incorrect_queries_llm = 0

    with open("Datasets/test_qald_10.json", 'r', encoding='utf-8') as dataset_file, open("Datasets/relationsQald10Test.txt", 'r', encoding='utf-8') as relations:
        qald10Test = json.load(dataset_file)
        output_data = {
        "dataset": {
            "id": "qald-X"
        },
        "questions": []
    }
        relation_lines = [line.strip() for line in relations]

        for question, relation in zip(qald10Test["questions"], relation_lines):
            sparql_query = question.get("query", {}).get("sparql", "")
            for q in question["question"]:
                if q["language"] == "en":
                    nl_question = q["string"]
                    break
            prompt = prompt_building(nl_question, relation)

            generated_sparql_query = get_sparql_from_gpt(prompt, gptmodel)
            llm_sparql_query = formate_output(generated_sparql_query)

            results_from_llm_query = run_sparql_query(llm_sparql_query)  
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
        
        with open("results" + gpt + ".json", "w", encoding="utf-8") as output_json_file:
            json.dump(output_data, output_json_file, indent=4, ensure_ascii=False)

 

if __name__ == "__main__":
    main("gpt-4-turbo")
