import matplotlib.pyplot as plt
import pandas as pd

# Create the dataframe
data = {
    "Gender": ["Andere", "Man", "Vrouw"],
    "0-25": [0, 9, 6],
    "26-45": [0, 26, 15],
    "46-65": [0, 46, 28],
    "65+": [1, 98, 36],
}
df = pd.DataFrame(data).set_index("Gender").T

# Extract the "Vrouw" and "Man" columns for plotting
vrouw_counts = df["Vrouw"]
man_counts = df["Man"]

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the female population (positive side)
plt.barh(vrouw_counts.index, vrouw_counts.values, color='red', edgecolor='black', label='Female (Vrouw)')

# Plot the male population (negative side)
plt.barh(man_counts.index, -man_counts.values, color='blue', edgecolor='black', label='Male (Man)')

# Add labels and title
plt.xlabel('Number of Respondents')
plt.ylabel('Age Category')
plt.title('Population by Age Category and Gender')

# Add gridlines for better readability
plt.grid(axis='x', linestyle='--', alpha=0.7, linewidth=0.5)

# Add a vertical line at x=0 for separation
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')

# Add a legend
plt.legend(loc='lower right')

# Show the plot
plt.tight_layout()
plt.show()
