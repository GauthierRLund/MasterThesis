import matplotlib.pyplot as plt

# Data from Table 7 (second image)
table7_metrics = ['Correct Property IDs', 'Correct Item IDs', 'Correct IDs (Both)']
table7_values = [154, 238, 130]

# Data from Table 19 (first image)
table19_metrics = ['Correct Property IDs', 'Correct Item IDs', 'Correct IDs (Both)']
table19_values = [235, 286, 211]

# X-axis positions for the two experiments
experiments = ['Baseline performance', 'Improved approached five-shot']

# Plotting
plt.figure(figsize=(10, 6))

# Plot lines for each metric
for i in range(len(table7_metrics)):
    plt.plot(experiments, [table7_values[i], table19_values[i]], marker='o', linestyle='-', label=table7_metrics[i])

# Customization
plt.xlabel('Experiments', fontsize=14, fontweight='bold')
plt.ylabel('Number of Queries', fontsize=14, fontweight='bold')
plt.title('Comparison of Correct IDs Across Experiments', fontsize=16, fontweight='bold')
plt.legend(fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# Show plot
plt.show()