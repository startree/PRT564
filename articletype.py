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

# Grouping the data by 'ArticleType' and calculating average and median duration days
article_type_stats = data.groupby('ArticleType')['DurationDays'].agg(['mean', 'median', 'count']).reset_index()

# Sort the results by median duration days for better comparison
article_type_stats_sorted = article_type_stats.sort_values(by='median', ascending=False)

print(article_type_stats_sorted)

