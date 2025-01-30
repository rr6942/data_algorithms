import pandas as pd

def find_column_matches(df1, df2):
    """
    Compare columns between two aligned DataFrames (same row count and order)
    Returns dictionary with best matches and counts
    """
    matches = {}
    
    # Convert to numpy arrays for position-wise comparison
    arr1 = df1.values  # Shape: (rows, df1_cols)
    arr2 = df2.values  # Shape: (rows, df2_cols)
    
    # Compare all columns simultaneously using broadcasting
    # This creates a 3D boolean array (df1_cols, df2_cols, rows)
    comparison = arr1[:, :, None] == arr2[:, None, :]
    
    # Count matches for each column pair
    match_counts = comparison.sum(axis=0)
    
    # Create results dictionary
    for i, col1 in enumerate(df1.columns):
        best_match_idx = match_counts[i].argmax()
        matches[col1] = {
            'matched_column': df2.columns[best_match_idx],
            'match_count': match_counts[i, best_match_idx],
            'all_matches': dict(zip(df2.columns, match_counts[i]))
        }
    
    return matches