import matplotlib.pyplot as plt
import numpy as np

# Data from the tables
metrics = ['Correct Property IDs', 'Correct Item IDs', 'Correct IDs (Both)']
table7_values = [170, 261, 146]
table20_values = [235, 286, 211]

# Plotting
x = np.arange(len(metrics))  # the label locations
width = 0.35  # the width of the bars

# Use a more sophisticated color palette
colors_table = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
colors_table1 = ['#aec7e8', '#ffbb78', '#98df8a']  # Lighter shades of the above

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, table7_values, width, color=colors_table)
rects2 = ax.bar(x + width/2, table20_values, width, color=colors_table1)

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Metrics')
ax.set_ylabel('Number of Queries')
ax.set_title('Performance Increase in terms of identifiers')
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.legend()

fig.tight_layout()

plt.show()