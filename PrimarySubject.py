import pandas as pd
from helperfunction import parse_dates
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import kruskal

# Load the dataset
datafile = 'retractions35215.csv'
data = pd.read_csv(datafile)

# Parse dates
data['OriginalPaperDate'] = parse_dates(data['OriginalPaperDate'])
data['RetractionDate'] = parse_dates(data['RetractionDate'])

# Function to map each primary subject to broader categories
def map_to_broader_category(subject):
    if pd.isnull(subject):
        return None
    prefix = subject.split(')')[0]
    categories = {
        'B/T': 'Business and Technology',
        'BLS': 'Basic Life Sciences',
        'ENV': 'Environmental Sciences',
        'HSC': 'Health Sciences',
        'HUM': 'Humanities',
        'PHY': 'Physical Sciences',
        'SOC': 'Social Sciences'
    }
    return categories.get(prefix, None)

# Apply mapping to broader categories
data['Subject'] = data['Subject'].apply(lambda x: x.split(';')[0].strip()[1:-1] if pd.notnull(x) else None)
data['PrimarySubject'] = data['Subject'].apply(map_to_broader_category)

# Calculate duration in days
data['Duration'] = (data['RetractionDate'] - data['OriginalPaperDate']).dt.days

# Basic statistics and boxplot visualization
primarysubject_duration_stats = data.groupby('PrimarySubject')['Duration'].describe()
plt.figure(figsize=(14, 8))
sns.boxplot(x='Duration', y='PrimarySubject', data=data, orient='h')
plt.title('Distribution of Durations from Publication to Retraction Across Primary Subjects')
plt.xlabel('Duration (Days)')
plt.ylabel('Primary Subject')
plt.tight_layout()
plt.show()

print(primarysubject_duration_stats)

# Kruskal-Wallis Test
# Group data by PrimarySubject and collect durations in a list for the Kruskal-Wallis test
durations_by_subject = [group["Duration"].dropna().values for name, group in data.groupby("PrimarySubject") if len(group["Duration"].dropna().values) > 2]

# Perform the Kruskal-Wallis test
stat, p_value = kruskal(*durations_by_subject)
print(f'Kruskal-Wallis Test Statistic: {stat}, p-value: {p_value}')