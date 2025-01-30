import pandas as pd
def simple_column_matcher(df1, df2, key_column):
    """Row-by-row comparison for accurate positional matching"""
    
    # Ensure perfect alignment using key column
    aligned = pd.merge(df1, df2, on=key_column, suffixes=('_1', '_2'))
    
    matches = {}
    
    # Compare columns pairwise
    for col1 in df1.columns:
        if col1 == key_column:
            continue
            
        best_count = 0
        best_match = None
        
        for col2 in df2.columns:
            if col2 == key_column:
                continue
                
            # Row-by-row comparison
            match_count = 0
            for i in range(len(aligned)):
                if aligned[col1].iloc[i] == aligned[col2].iloc[i]:
                    match_count += 1
                    
            if match_count > best_count:
                best_count = match_count
                best_match = col2
                
        matches[col1] = {
            'best_match': best_match,
            'match_count': best_count
        }
    
    return matches