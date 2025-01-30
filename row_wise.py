import pandas as pd

# Sample data (replace with your actual data)
df1 = pd.DataFrame({
    'CustomerID': [101, 102, 103],
    'Revenue': [500, 600, 700],
    'OrderDate': ['2024-05-01', '2024-05-01', '2024-05-01'],
    'UnmatchedColumn': [1, 2, 3]  # No match in df2
})

df2 = pd.DataFrame({
    'XXBHS': [101, 102, 103],       # Matches CustomerID
    'Sales': [500, 600, 700],       # Matches Revenue
    'DT_123': ['2024-05-01', '2024-05-01', '2024-05-01'],  # Matches OrderDate
    'RandomColumn': [10, 20, 30]    # No match
})

# ---------------------------------------------------------------
# Matching Logic
# ---------------------------------------------------------------
def match_columns(df1, df2):
    matches = {}
    
    for source_col in df1.columns:
        max_matches = 0
        best_match = None
        
        for target_col in df2.columns:
            # Compare values row-wise (exact matches)
            match_count = (df1[source_col].astype(str) == df2[target_col].astype(str)).sum()
            
            # Update best match if this column has more matches
            if match_count > max_matches:
                max_matches = match_count
                best_match = target_col
            elif match_count == max_matches and max_matches > 0:
                # Tiebreaker: Use the first encountered column
                if best_match is None:
                    best_match = target_col
        
        matches[source_col] = {
            'df2_column': best_match,
            'exact_matches': max_matches
        }
    
    return matches

# ---------------------------------------------------------------
# Run the matcher
# ---------------------------------------------------------------
result = match_columns(df1, df2)

# Print results
print("Column Matches:")
for col, info in result.items():
    print(f"{col}:")
    print(f"  → Matches '{info['df2_column']}' with {info['exact_matches']} exact row-wise matches\n")