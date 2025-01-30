def safe_column_matcher(df1, df2, key_col_df1, key_col_df2):
    """Compare columns with different key column names and type safety"""
    # Convert keys to string type to prevent type mismatch
    df1 = df1.astype({key_col_df1: str})
    df2 = df2.astype({key_col_df2: str})
    
    # Merge on different key column names
    merged = pd.merge(
        df1, df2, 
        left_on=key_col_df1, 
        right_on=key_col_df2,
        suffixes=('_df1', '_df2')
    )
    
    matches = {}
    
    # Compare non-key columns
    for col1 in df1.columns:
        if col1 == key_col_df1:
            continue
            
        best_match = None
        max_count = 0
        
        for col2 in df2.columns:
            if col2 == key_col_df2:
                continue
                
            # Type-safe comparison
            match_count = 0
            for i in range(len(merged)):
                # Convert both values to string for safe comparison
                val1 = str(merged[col1].iloc[i])
                val2 = str(merged[col2].iloc[i])
                
                if val1 == val2:
                    match_count += 1
            
            # Handle ties by column name (now both strings)
            if match_count > max_count or \
               (match_count == max_count and col2 < str(best_match)):
                max_count = match_count
                best_match = col2
        
        matches[col1] = {
            'best_match': best_match,
            'match_count': max_count,
            'match_percentage': f"{(max_count/len(merged))*100:.1f}%"
        }
    
    return matches