import pandas as pd

# Sample DataFrame
data = {
    'ID': [1, 2, 3, 4, 5],
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 25, 30],
    'City': ['New York', 'Los Angeles', 'Chicago', 'New York', 'Los Angeles']
}

df = pd.DataFrame(data)

# Function to find columns with unique values
def find_unique_columns(df):
    # Calculate the number of unique values in each column
    unique_counts = df.nunique()
    
    # Identify columns where the number of unique values equals the number of rows
    unique_columns = unique_counts[unique_counts == len(df)]
    
    return unique_columns

# Find and print columns with unique values
unique_columns = find_unique_columns(df)

if not unique_columns.empty:
    print("Columns with unique values:")
    print(unique_columns)
else:
    print("No columns with unique values found.")

# Verify uniqueness by checking for duplicates
for column in df.columns:
    if df[column].duplicated().any():
        print(f"Column '{column}' has duplicates.")
    else:
        print(f"Column '{column}' is unique.")
