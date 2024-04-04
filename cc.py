import pandas as pd

# Read the CSV file and store it in a DataFrame
data = pd.read_csv("retractions35215.csv")

# Print the contents of the DataFrame
print(data.head())

data = data.head(200)
print(data)
