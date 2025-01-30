def column_matcher(df1, df2, use_row_alignment=False, threshold=0.8):
    """Robust column matcher with error fixes"""
    results = {}  # Stores final matches
    
    # 1. Handle zero columns
    zero_cols_df1 = [col for col in df1 if (df1[col] == '0').all()]
    zero_cols_df2 = [col for col in df2 if (df2[col] == '0').all()]
    
    for z_col in zero_cols_df1:
        for candidate in zero_cols_df2:
            if candidate not in results.values():
                results[z_col] = candidate
                zero_cols_df2.remove(candidate)
                break
    
    # 2. Handle remaining columns
    remaining_df1 = df1.drop(columns=zero_cols_df1)
    remaining_df2 = df2.drop(columns=zero_cols_df2 + list(results.values()))
    
    for col1 in remaining_df1.columns:
        best_match = None
        max_score = 0
        
        for col2 in remaining_df2.columns:
            if use_row_alignment:
                # Row-aligned comparison
                match_count = sum(1 for i in range(len(df1)) 
                                if df1[col1].iloc[i] == df2[col2].iloc[i])
                score = match_count / len(df1)
            else:
                # Set-based comparison
                set1 = set(remaining_df1[col1].dropna())
                set2 = set(remaining_df2[col2].dropna())
                score = len(set1 & set2) / max(len(set1), 1)
            
            if score > max_score and score >= threshold:
                max_score = score
                best_match = col2
        
        if best_match:
            results[col1] = best_match
            remaining_df2 = remaining_df2.drop(columns=[best_match])
    
    return results