import pandas as pd
from collections import defaultdict

# Sample data (replace with your actual data)
df1 = pd.DataFrame({
    'CustomerID': [101, 102, 103, 104],       # 4 values
    'Product': ['A', 'B', 'C', 'D'],          # 4 values
    'Revenue': [500, 600, 700, 800],          # 4 values
    'Unmatched': [1, 2, 3, 4]                # No match in df2
})

df2 = pd.DataFrame({
    'XXBHS': [101, 102, 103, 999],            # 3/4 matches with CustomerID
    'Sales': [500, 600, 700, 800],            # 4/4 matches with Revenue
    'Item': ['A', 'B', 'C', 'X'],             # 3/4 matches with Product
    'Random1': [10, 20, 30, 40],              # No matches
    'Random2': ['X', 'Y', 'Z', 'W']           # No matches
})

def find_column_matches(df1, df2):
    # Convert all values to strings to handle type mismatches
    df1 = df1.astype(str)
    df2 = df2.astype(str)
    
    # Precompute sets for df2 columns
    df2_sets = {col: set(df2[col].dropna()) for col in df2.columns}
    
    # Track best matches for df1 columns
    matches = {}
    
    for col1 in df1.columns:
        # Get unique values for the df1 column
        values_df1 = set(df1[col1].dropna())
        best_match = None
        max_overlap = 0
        
        # Compare with all df2 columns
        for col2, values_df2 in df2_sets.items():
            overlap = len(values_df1 & values_df2)
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = col2
        
        # Store results (even if no matches)
        matches[col1] = {
            'df2_column': best_match,
            'overlap_count': max_overlap
        }
    
    return matches

# Run the matcher
results = find_column_matches(df1, df2)

# Print results
print("Column Matches (Value Overlap):")
for col, info in results.items():
    print(f"{col} → {info['df2_column']} (Overlap: {info['overlap_count']})")