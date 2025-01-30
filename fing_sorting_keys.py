def find_sorting_key(df1, df2):
    """
    Find columns with identical values (potential primary keys) 
    to use for row alignment
    """
    potential_keys = []
    
    for col1 in df1.columns:
        for col2 in df2.columns:
            # Check for exact value matches (order-agnostic)
            if set(df1[col1]) == set(df2[col2]):
                potential_keys.append((col1, col2))
    
    # Return first pair found, or None
    return potential_keys[0] if potential_keys else (None, None)

# Usage:
sort_key_df1, sort_key_df2 = find_sorting_key(df1, df2)