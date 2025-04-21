import matplotlib.pyplot as plt
import numpy as np

# Data from the tables
triples = [1, 2, 3, 4, 5, 7]
gold_queries = [249, 98, 35, 8, 2, 2]
llm_queries_total = [166, 48, 5, 0, 0, 0]  # Total LLM Queries
correct_llm_queries = [158, 33, 6, 2, 0, 0]  # Correct LLM Queries

x = np.arange(len(triples))  # the label locations
width = 0.25  # the width of the bars

# Define a modern and harmonious color palette
colors = ['#1f77b4', '#2ca02c', '#ff7f0e']  # Blue, Orange, Green

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width, gold_queries, width, label='Number of gold Queries', color=colors[0], edgecolor='black')
rects2 = ax.bar(x, llm_queries_total, width, label='Number of queries with the correct number of triple patterns Improved approach five-shot', color=colors[1], edgecolor='black')
rects3 = ax.bar(x + width, correct_llm_queries, width, label='Number of queries with the correct number of triple patterns Baseline results', color=colors[2], edgecolor='black')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Number of Triple patterns', fontsize=12)
ax.set_ylabel('Number of Queries', fontsize=12)
ax.set_title('Number of LLM Queries with the correct number of triple patterns', fontsize=14, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(triples, fontsize=12)
ax.legend(fontsize=12)

# Add grid lines for better readability
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Customize the spines (borders)
for spine in ax.spines.values():
    spine.set_edgecolor('#333333')

# Add some padding for better visualization
plt.tight_layout()

plt.show()