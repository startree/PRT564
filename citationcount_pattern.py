# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score

# Read the document data
data = pd.read_csv("retractions35215.csv")  # Please replace "your_document.csv" with the path to your document file
# Assume the data includes three categorical features and a continuous numerical target value
data = data.head(2000)
print(data)
X = data[['Journal', 'Publisher', 'Country']]  # Select columns containing categorical features
y = data['CitationCount']  # Target variable is a continuous numerical value

# Perform one-hot encoding on all categorical features
X_encoded = pd.get_dummies(X, columns=['Journal', 'Publisher', 'Country'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Initialize the SVR model
model = SVR()

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate mean squared error and R^2 score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Output performance metrics
print("Mean Squared Error: {:.2f}".format(mse))
print("R^2 Score: {:.2f}".format(r2))
