import pandas as pd

def find_best_column_matches(df1, df2):
    """
    Compare columns between two aligned DataFrames row-wise and find the best matches.
    
    Args:
        df1 (pd.DataFrame): First DataFrame (columns to match FROM)
        df2 (pd.DataFrame): Second DataFrame (columns to match TO)
    
    Returns:
        dict: Mapping of df1 columns to their best df2 matches with match counts
    """
    matches_dict = {}
    
    # Compare each column in df1 with all columns in df2
    for df1_col in df1.columns:
        max_matches = 0
        best_match = None
        
        for df2_col in df2.columns:
            # Count matching values between the two columns
            match_count = (df1[df1_col] == df2[df2_col]).sum()
            
            # Update best match if current is better
            if match_count > max_matches or (match_count == max_matches and df2_col < best_match):
                max_matches = match_count
                best_match = df2_col
        
        # Store results (even if no matches found)
        matches_dict[df1_col] = {
            'matched_column': best_match,
            'match_count': max_matches
        }
    
    return matches_dict

# Example usage:
# matches = find_best_column_matches(df