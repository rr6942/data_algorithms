import pandas as pd

# Hardcoded column names (replace with your actual column names)
column_names = ['Name', 'Age', 'City', "Savings", "Spending"]

# Hardcoded dataframes for testing
df1 = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago'],
    "Savings": [0, 0, 2],
    "Spending": [0, 10, 10]}
)

df2 = pd.DataFrame({
    'Full Name': ['Alice', 'Bob', 'Charlie'],
    'Years': [25, 30, 35],
    'Location': ['New York', 'Los Angeles', 'Chicago'],
    "Savings_USD": [0, 0, 2],
    "Spending_EUR": [0, 10, 10]
})

# Dictionary to store matching columns
matching_columns = {}

# Iterate through the column names
for col1_name in column_names:
    if col1_name in df1.columns:
        # Get the values from the column in df1
        col1_values = df1[col1_name]
        
        # Search for these values in df2
        for col2_name in df2.columns:
            col2_values = df2[col2_name]
            
            # Check if the values match exactly
            if col1_values.equals(col2_values):
                matching_columns[col1_name] = col2_name
                break  # Stop searching once a match is found
    else:
        print(f"Column '{col1_name}' not found in df1.")

# Print the matching columns
print("Matching columns:")
print(matching_columns)