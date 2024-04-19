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

# Function to get top 10 with highest counts for each category and calculate their mean and median for DurationDays
def top_10_stats(data, category):
    top_10 = data[category].value_counts().head(10).index
    top_10_stats = data[data[category].isin(top_10)].groupby(category).agg({
        'DurationDays': ['mean', 'median'],
        'CitationCount': ['mean', 'median'],
        'Record ID': 'count'
    }).sort_values(by=('Record ID', 'count'), ascending=False)
    return top_10_stats

# Top 10 statistics for each characteristics
top_10_subject_stats = top_10_stats(data, 'Subject')
data['Institution'] = data['Institution'].replace(['unavailable', 'Unavailable', 'Unknown'], 'Unavailable/Unknown')
top_10_institution_stats = top_10_stats(data, 'Institution')
top_10_journal_stats = top_10_stats(data, 'Journal')
top_10_publisher_stats = top_10_stats(data, 'Publisher')
top_10_country_stats = top_10_stats(data, 'Country')
top_10_article_type_stats = top_10_stats(data, 'ArticleType')

print(top_10_subject_stats)
print(top_10_institution_stats)
print(top_10_journal_stats)
print(top_10_publisher_stats)
print(top_10_country_stats)
print(top_10_article_type_stats)

# Calculate the mean and median for the DurationDays and CitationCount for the entire dataset
duration_mean = data['DurationDays'].mean()
duration_median = data['DurationDays'].median()
citation_mean = data['CitationCount'].mean()
citation_median = data['CitationCount'].median()

print("\nOverall Duration Mean: ", duration_mean, "\nOverall Duration Median: ", duration_median)
print("\nOverall Citation Mean: ", citation_mean, "\nOverall Citation Median: ", citation_median)


import matplotlib.pyplot as plt
import seaborn as sns

# Filter the data for top 10 institutions based on count
top_10_institutions = data['Institution'].value_counts().nlargest(10).index
filtered_institution_data = data[data['Institution'].isin(top_10_institutions)]

plt.figure(figsize=(12, 8))
sns.violinplot(x='DurationDays', y='Institution', data=filtered_institution_data, scale='width', inner='quartile')
plt.title('Distribution of Duration Days Across Top 10 Institutions')
plt.xlabel('Duration Days')
plt.ylabel('Institution')
plt.show()

# Filter the data for top 10 publishers based on count
top_10_publishers = data['Publisher'].value_counts().nlargest(10).index
filtered_publisher_data = data[data['Publisher'].isin(top_10_publishers)]

plt.figure(figsize=(12, 8))
sns.violinplot(x='DurationDays', y='Publisher', data=filtered_publisher_data, scale='width', inner='quartile')
plt.title('Distribution of Duration Days Across Top 10 Publishers')
plt.xlabel('Duration Days')
plt.ylabel('Publisher')
plt.show()

# Filter the data for top 10 journals based on count
top_10_journals = data['Journal'].value_counts().nlargest(10).index
filtered_journal_data = data[data['Journal'].isin(top_10_journals)]

plt.figure(figsize=(12, 8))
sns.violinplot(x='DurationDays', y='Journal', data=filtered_journal_data, scale='width', inner='quartile')
plt.title('Distribution of Duration Days Across Top 10 Journals')
plt.xlabel('Duration Days')
plt.ylabel('Journal')
plt.show()

# Filter the data for top 10 countries based on count
top_10_countries = data['Country'].value_counts().nlargest(10).index
filtered_country_data = data[data['Country'].isin(top_10_countries)]

plt.figure(figsize=(12, 8))
sns.violinplot(x='DurationDays', y='Country', data=filtered_country_data, scale='width', inner='quartile')
plt.title('Distribution of Duration Days Across Top 10 Countries')
plt.xlabel('Duration Days')
plt.ylabel('Country')
plt.show()

# Filter the data for top 10 article types based on count
top_10_article_types = data['ArticleType'].value_counts().nlargest(10).index
filtered_article_type_data = data[data['ArticleType'].isin(top_10_article_types)]

plt.figure(figsize=(12, 8))
sns.violinplot(x='DurationDays', y='ArticleType', data=filtered_article_type_data, scale='width', inner='quartile')
plt.title('Distribution of Duration Days Across Top 10 Article Types')
plt.xlabel('Duration Days')
plt.ylabel('Article Type')
plt.show()

# Creating a DataFrame from the stats
df_stats = top_10_institution_stats.reset_index()
df_stats.columns = ['Institution', 'Duration Mean', 'Duration Median', 'Citation Mean', 'Citation Median', 'Count']

# Plotting DurationDays and CitationCount distributions
plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)
sns.boxplot(data=df_stats, y='Duration Median')
plt.title('Distribution of Duration Days (Median)')

plt.subplot(1, 2, 2)
sns.boxplot(data=df_stats, y='Citation Median')
plt.title('Distribution of Citation Counts (Median)')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_stats, x='Duration Mean', y='Citation Mean', size='Count', hue='Institution', legend=False, sizes=(100, 2000))
plt.xlabel('Mean Duration Days')
plt.ylabel('Mean Citation Counts')
plt.title('Mean Duration Days vs. Mean Citation Counts by Institution')
plt.grid(True)
plt.show()
