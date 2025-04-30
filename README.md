# MasterThesis
This thesis aims to evaluate the performance of GPT-4-Turbo and a fine-tuned version of GPT-4o in terms of generating SPARQL queries. Our experiments were conducted on the QALD-10 dataset, using the GERBIL benchmarking framework to evaluate the results. The GPT-4o model was fine-tuned on the QALD-10 training set.

# Approach 
We replicated the approach from the paper "Generating SPARQL from Natural Language Using Chain-of-Thoughts" to establish a baseline performance. An error analysis was then performed by categorizing errors into four types: patterns, keywords, identifiers, and syntax errors.

# Prompt 
Based on this error analysis, we designed two new experiments aimed at reducing these specific error types.
![image](https://github.com/user-attachments/assets/3db0a3de-1172-48b0-8d0b-8451cf6f709c)

# Results 
The new experiments, evaluated using the GERBIL benchmarking framework, yielded the following results:
![image](https://github.com/user-attachments/assets/e213db83-e6ee-4558-80f4-0b0a30d2e88b)

# Supplementary experiments
Additionally, we conducted four supplementary experiments to further evaluate model performance when provided with: gold identifiers, gold keywords, the number of triple patterns.
The results of the supplementary experiments were as following.
![image](https://github.com/user-attachments/assets/921fe827-5bf2-4590-9581-b1346e6bfde9)

# Running the project 
```
git clone https://github.com/GauthierRLund/MasterThesis.git
pip install -r requirements.txt
```
