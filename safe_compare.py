import pandas as pd
import numpy as np
from collections import defaultdict

def safe_compare(a, b):
    """Compare values safely (handles different types and NaNs)"""
    try:
        return str(a).strip().lower() == str(b).strip().lower()
    except:
        return False

def find_column_matches(df1, df2, threshold=0.7):
    """
    Match columns between df1 and df2 based on row-wise value matches.
    Args:
        threshold: Minimum % of matching rows required (0-1)
    Returns:
        Dict: {df1_column: {'match': df2_column, 'confidence': float}}
    """
    # Preprocessing
    df1 = df1.fillna('__NA__').astype(str)
    df2 = df2.fillna('__NA__').astype(str)
    
    # Track best matches and used columns
    matches = {}
    used_df2_columns = set()
    
    # Special case: Zero-value columns
    zero_cols_df1 = [col for col in df1 if (df1[col] == '0').all()]
    zero_cols_df2 = [col for col in df2 if (df2[col] == '0').all()]
    
    # First handle zero columns
    for z_col in zero_cols_df1:
        for candidate in zero_cols_df2:
            if candidate not in used_df2_columns:
                matches[z_col] = {'match': candidate, 'confidence': 1.0}
                used_df2_columns.add(candidate)
                break
    
    # For non-zero columns
    for col1 in df1.columns:
        if col1 in matches:
            continue  # Skip already matched zero columns
            
        best_match = None
        max_matches = 0
        total_rows = len(df1)
        
        for col2 in df2.columns:
            if col2 in used_df2_columns:
                continue
                
            # Count row-wise matches
            match_count = sum(safe_compare(df1[col1].iloc[i], df2[col2].iloc[i]) 
                            for i in range(len(df1)))
            
            if match_count > max_matches:
                max_matches = match_count
                best_match = col2
        
        # Check threshold
        confidence = max_matches / total_rows
        if confidence >= threshold and best_match:
            matches[col1] = {
                'match': best_match,
                'confidence': round(confidence, 2)
            }
            used_df2_columns.add(best_match)
        else:
            matches[col1] = {'match': None, 'confidence': 0}
    
    return matches

# Example usage
if __name__ == "__main__":
    # Sample data with edge cases
    df1 = pd.DataFrame({
        'CustomerID': ['101', '102', '103'],
        'Revenue': ['500', '600', '700'],
        'ZeroColumn': ['0', '0', '0'],
        'Date': ['2023-01-01', '2023-02-01', '2023-03-01']
    })
    
    df2 = pd.DataFrame({
        'CUST_ID': ['101', '102', '103'],  # Match CustomerID
        'SALES': ['500', '600', '700'],     # Match Revenue
        'ALL_ZEROS': ['0', '0', '0'],       # Match ZeroColumn
        'TRANS_DATE': ['2023-01-01', '2023-02-01', '2023-03-01'],  # Match Date
        'UNRELATED': ['A', 'B', 'C']        # No match
    })

    results = find_column_matches(df1, df2, threshold=0.5)
    
    print("Column Matches:")
    for col, match_info in results.items():
        print(f"{col} → {match_info['match']} (Confidence: {match_info['confidence']:.0%})")