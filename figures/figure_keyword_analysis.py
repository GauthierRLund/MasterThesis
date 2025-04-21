import matplotlib.pyplot as plt
import numpy as np

# Summed-up values from Table 9 (GPT-4-Turbo)
table9_sums = {
    "TP": 215,
    "TN": 4435,
    "FP": 136,
    "FN": 136,
}

# Summed-up values from Table 21 (GPT-4o)
table21_sums = {
    "TP": 273,  # Sum of TP values from Table 21
    "TN": 4498,  # Sum of TN values from Table 21
    "FP": 73,    # Sum of FP values from Table 21
    "FN": 78,    # Sum of FN values from Table 21
}

# Metrics to compare
metrics_tn = ["TN"]
metrics_others = ["TP", "FP", "FN"]

# Values for Table 9 and Table 21
table9_values_tn = [table9_sums[metric] for metric in metrics_tn]
table21_values_tn = [table21_sums[metric] for metric in metrics_tn]

table9_values_others = [table9_sums[metric] for metric in metrics_others]
table21_values_others = [table21_sums[metric] for metric in metrics_others]

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Subplot 1: TN
x_tn = np.arange(len(metrics_tn))
width = 0.35
ax1.bar(x_tn - width/2, table9_values_tn, width, color='#1f77b4')
ax1.bar(x_tn + width/2, table21_values_tn, width, color='#aec7e8')
ax1.set_xlabel('Metrics')
ax1.set_ylabel('Counts')
ax1.set_title('True Negatives (TN)')
ax1.set_xticks(x_tn)
ax1.set_xticklabels(metrics_tn)
ax1.legend()

# Subplot 2: TP, FP, FN
x_others = np.arange(len(metrics_others))
ax2.bar(x_others - width/2, table9_values_others, width, color=['#ff7f0e', '#2ca02c', '#d62728'])
ax2.bar(x_others + width/2, table21_values_others, width, color=['#ffbb78', '#98df8a', '#ff9896'])
ax2.set_xlabel('Metrics')
ax2.set_ylabel('Counts')
ax2.set_title('TP, FP, FN')
ax2.set_xticks(x_others)
ax2.set_xticklabels(metrics_others)
ax2.legend()

# Add value labels on top of the bars
def add_labels(ax, bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(ax1, ax1.patches)
add_labels(ax2, ax2.patches)

fig.tight_layout()
plt.show()