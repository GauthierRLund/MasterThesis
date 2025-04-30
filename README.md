# MasterThesis
This thesis analyzes the performance of GPT-4-Turbo and a fine-tuned GPT-4o model in generating SPARQL queries. Our experiments were conducted on the QALD-10 dataset, using the GERBIL benchmarking framework to evaluate the results. The GPT-4o model was fine-tuned using the QALD-10 training set.

We replicated the approach from the paper "Generating SPARQL from Natural Language Using Chain-of-Thoughts" to establish a baseline. An error analysis was then performed by categorizing errors into four types: patterns, keywords, identifiers, and syntax errors.

Based on this analysis, we designed a new experiment aimed at reducing these specific error types through targeted mitigation strategies.
![image](https://github.com/user-attachments/assets/3db0a3de-1172-48b0-8d0b-8451cf6f709c)
The new experiments, evaluated using the GERBIL benchmarking framework, yielded the following results:
![image](https://github.com/user-attachments/assets/e213db83-e6ee-4558-80f4-0b0a30d2e88b)

To run the project, simply clone the project and do pip install -r requirements.txt
Additionally, we conducted four supplementary experiments to further evaluate model performance when provided with: gold identifiers, gold keywords, the number of triple patterns.
