import pandas as pd
#converts the 'Subject' column to string format, 
# splits the column containing multiple labels into separate labels, 
# and then finds and prints out the total number of unique labels and the list of unique labels.


# Example data
data = pd.read_csv("retractions35215.csv") 

#data = data.head(2000)

df = pd.DataFrame(data)

# Convert the data column to string format
df['Subject'] = df['Subject'].astype(str)

# Split the column containing multiple labels into separate labels
df['Subject'] = df['Subject'].str.split(';')

# Find the different labels
all_labels_flat = [label for sublist in df['Subject'] for label in sublist]
unique_labels = set(all_labels_flat)
num_unique_labels = len(unique_labels)

print("Total number of unique labels: ", num_unique_labels)
print("Unique labels: ", unique_labels)
