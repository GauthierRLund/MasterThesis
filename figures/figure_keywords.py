import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Data from the table
data = {
    "Keyword": ["FILTER", "ORDER BY ASC", "LIMIT", "ASK", "UNION", "MINUS", "COUNT", "GROUP BY", "ORDER BY DESC", "YEAR", "OFFSET", "OPTIONAL", "BIND"],
    "Gold Count": [77, 9, 20, 60, 5, 2, 100, 3, 11, 26, 3, 1, 34],
    "TP": [49, 0, 16, 60, 1, 0, 98, 3, 10, 21, 2, 0, 13],
    "TN": [301, 385, 362, 327, 387, 392, 278, 386, 374, 365, 391, 390, 360],
    "FP": [16, 0, 12, 7, 2, 0, 16, 5, 9, 3, 0, 3, 0],
    "FN": [28, 9, 4, 0, 4, 2, 2, 0, 1, 5, 1, 1, 21]
}

# Convert to a DataFrame
df = pd.DataFrame(data)

# Set up the figure and subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Keyword Analysis for GPT-4o", fontsize=16, y=1.02)  # Adjust title position

# Plot each metric in a separate subplot
metrics = ["TP", "FP", "TN", "FN"]
titles = ["True Positives (TP)", "False Positives (FP)", "True Negatives (TN)", "False Negatives (FN)"]
colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]  # Nicer color scheme

for i, ax in enumerate(axes.flatten()):
    sns.barplot(x="Keyword", y=metrics[i], data=df, ax=ax, color=colors[i])
    ax.set_title(titles[i], fontsize=14, pad=10)  # Add padding to titles
    ax.set_ylabel("Count", fontsize=12)
    ax.tick_params(axis="x", rotation=45, labelsize=10)  # Rotate x-axis labels for better readability
    ax.tick_params(axis="y", labelsize=10)
    ax.set_xlabel("")  # Remove x-axis label

# Adjust layout to prevent overlapping
plt.tight_layout()
plt.show()