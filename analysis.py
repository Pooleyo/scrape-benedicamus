import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('data/inference/inference_results.csv')

# Set up the plot
plt.figure(figsize=(12, 6))

# Plot the distribution of probabilities for "has_benedicamus"
sns.histplot(df['has_benedicamus_probability'], kde=True, color='blue', alpha=0.5, label='Has Benedicamus')

# Plot the distribution of probabilities for "does_not_have_benedicamus"
sns.histplot(df['does_not_have_benedicamus_probability'], kde=True, color='red', alpha=0.5, label='Does Not Have Benedicamus')

# Customize the plot
plt.title('Distribution of Benedicamus Probabilities')
plt.xlabel('Probability')
plt.ylabel('Frequency')
plt.legend()

# Save the plot
plt.savefig('data/inference/probability_distribution.png')
plt.close()

print("Distribution plot saved as 'data/inference/probability_distribution.png'")
