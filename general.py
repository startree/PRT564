import pandas as pd
from helperfunction import parse_dates

# Load the dataset
datafile = 'retractions35215.csv'
data = pd.read_csv(datafile)

# Apply the date parsing helper function
data['RetractionDate'] = parse_dates(data['RetractionDate'])
data['OriginalPaperDate'] = parse_dates(data['OriginalPaperDate'])

# Recalculate the duration in days
data['DurationDays'] = (data['RetractionDate'] - data['OriginalPaperDate']).dt.days

# Compute the average duration from publication to retraction for selected characteristics
characteristics = ['Subject', 'Journal', 'Institution', 'Country', 'ArticleType', 'Publisher']
avg_durations = {feature: data.groupby(feature)['DurationDays'].mean().sort_values(ascending=False) for feature in characteristics}

# For demonstration, let's display the top 5 categories by average duration for each characteristic
top_avg_durations = {feature: avg[avg > 0][:5] for feature, avg in avg_durations.items()}  # Filtering avg > 0 to remove any with no duration

print(top_avg_durations)
