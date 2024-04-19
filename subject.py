import pandas as pd
from helperfunction import parse_dates
from collections import Counter

# Load the dataset
datafile = 'retractions35215.csv'
data = pd.read_csv(datafile)

# Apply the date parsing helper function
data['RetractionDate'] = parse_dates(data['RetractionDate'])
data['OriginalPaperDate'] = parse_dates(data['OriginalPaperDate'])

# Recalculate the duration in days
data['DurationDays'] = (data['RetractionDate'] - data['OriginalPaperDate']).dt.days

# Normalize and split 'Subject' column into a list of subjects for each row
data['Subjects'] = data['Subject'].str.lower().str.split(';').apply(lambda x: [subject.strip() for subject in x])

# Flatten the list of all subjects and count each occurrence
all_subjects_flat = [subject for sublist in data['Subjects'] for subject in sublist if subject]
subject_counts = Counter(all_subjects_flat)

# Convert the counts to a DataFrame for easier analysis, and sort to find the top 20 subjects
subject_counts_df = pd.DataFrame(subject_counts.items(), columns=['Subject', 'Count']).sort_values(by='Count', ascending=False)

# Extract the top 20 subjects
top_20_subjects = subject_counts_df.head(20)['Subject'].tolist()

# Initialize a list to hold the mean and median for each of the top 20 subjects along with their count
subject_duration_stats = []

for subject in top_20_subjects:
    # Filter the dataset for each subject.
    subject_mask = data['Subjects'].apply(lambda x: subject in x)
    filtered_data = data[subject_mask]
    
    # Calculate mean and median duration days for the filtered dataset
    mean_duration = filtered_data['DurationDays'].mean()
    median_duration = filtered_data['DurationDays'].median()
    
    # Get the count from subject_counts_df
    subject_count = subject_counts_df[subject_counts_df['Subject'] == subject]['Count'].values[0]
    
    # Append the results
    subject_duration_stats.append({
        'Subject': subject,
        'Count': subject_count,
        'MeanDurationDays': mean_duration,
        'MedianDurationDays': median_duration
    })

# Convert the list to a DataFrame for display
subject_duration_stats_df = pd.DataFrame(subject_duration_stats)
print(subject_duration_stats_df)
