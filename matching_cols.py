import pandas as pd

# Sample DataFrames
df1 = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
})

df2 = pd.DataFrame({
    'Full Name': ['Alice', 'Bob', 'Charlie'],
    'Years': [25, 30, 36],
    'Location': ['New York', 'Los Angeles', 'Chicago']
})

# Function to compare columns
def compare_columns(df1, df2):
    matching_columns = {}
    
    # Iterate through each column in df1
    for col1_name in df1.columns:
        # Iterate through each column in df2
        for col2_name in df2.columns:
            # Check if the columns are identical
            if df1[col1_name].equals(df2[col2_name]):
                matching_columns[col1_name] = col2_name
    
    return matching_columns

# Find and print matching columns
matching_columns = compare_columns(df1, df2)

if matching_columns:
    print("Matching columns:")
    print(matching_columns)
else:
    print("No matching columns found.")
