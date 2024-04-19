import pandas as pd
from helperfunction import parse_dates

import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file = 'retractions35215.csv'
retraction_data = pd.read_csv(file)

# Apply the date parsing helper function
retraction_data['RetractionDate'] = parse_dates(retraction_data['RetractionDate'])
retraction_data['OriginalPaperDate'] = parse_dates(retraction_data['OriginalPaperDate'])

# Recalculate the duration in days
retraction_data['DurationDays'] = (retraction_data['RetractionDate'] - retraction_data['OriginalPaperDate']).dt.days

# Displaying the updated dataframe with the new 'DurationDays' column
print(retraction_data[['Record ID', 'RetractionDate', 'OriginalPaperDate', 'DurationDays']].head())

# Plotting the distribution of DurationDays
plt.figure(figsize=(14, 7))
sns.histplot(retraction_data['DurationDays'].dropna(), kde=True, bins=50, color='skyblue')
plt.title('Distribution of Duration from Publication to Retraction (in days)')
plt.xlabel('Duration in Days')
plt.ylabel('Frequency')
plt.show()

# Plotting the distribution of CitationCount
plt.figure(figsize=(14, 7))
sns.histplot(retraction_data['CitationCount'].dropna(), kde=True, bins=50, color='salmon')
plt.title('Distribution of Citation Counts of Retracted Papers')
plt.xlabel('Citation Count')
plt.ylabel('Frequency')
plt.xscale('log') # Using log scale due to the wide range of citation counts
plt.show()

# Summary statistics for DurationDays and CitationCount
duration_citation_summary = retraction_data[['DurationDays', 'CitationCount']].describe()

print(duration_citation_summary)