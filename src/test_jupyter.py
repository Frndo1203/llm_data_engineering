#%%
# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [24, 27, 22, 32, 29],
    'Score': [85, 90, 88, 76, 95]
}
df = pd.DataFrame(data)
# %%
# Display the first few rows of the DataFrame
print("First few rows of the DataFrame:")
print(df.head())

# Describe the data
print("\nDescriptive statistics of the DataFrame:")
print(df.describe())

# Filter the data (e.g., select rows where Age > 25)
filtered_df = df[df['Age'] > 25]
print("\nFiltered DataFrame (Age > 25):")
print(filtered_df)
#%%
# Plot the data
plt.figure(figsize=(10, 5))
plt.bar(df['Name'], df['Score'], color='blue')
plt.xlabel('Name')
plt.ylabel('Score')
plt.title('Scores by Name')
plt.show()
# %%
