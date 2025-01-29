import pandas as pd
from collections import defaultdict

# Sample data (replace with your actual data)
snowflake_data = pd.DataFrame({
    'CustomerID': [101, 102, 103],
    'Revenue': [500, 600, 700],
    'OrderDate': ['2024-05-01', '2024-05-01', '2024-05-01']
})

celonis_data = pd.DataFrame({
    'XXBHS': [101, 102, 103],       # Matches CustomerID
    'Sales': [500, 600, 700],       # Matches Revenue
    'DT_123': ['2024-05-01', '2024-05-01', '2024-05-01']  # Matches OrderDate
})

# ---------------------------------------------------------------
# Matching Logic
# ---------------------------------------------------------------
def match_columns(source_df, target_df, threshold=0.5):
    matches = {}
    used_target_cols = set()
    
    # Track scores: {source_col: {target_col: match_score}}
    score_matrix = defaultdict(dict)
    
    # Compare all source columns to target columns
    for source_col in source_df.columns:
        source_values = source_df[source_col].dropna().astype(str).tolist()
        
        for target_col in target_df.columns:
            if target_col in used_target_cols:
                continue  # Skip already matched columns
            
            target_values = target_df[target_col].dropna().astype(str).tolist()
            
            # Count overlapping values
            overlap = len(set(source_values) & set(target_values))
            total = max(len(source_values), 1)  # Avoid division by zero
            score = overlap / total
            
            score_matrix[source_col][target_col] = score
    
    # Assign best matches (prioritize highest scores)
    for source_col in sorted(score_matrix, key=lambda x: max(score_matrix[x].values(), default=0), reverse=True):
        target_cols = score_matrix[source_col]
        if not target_cols:
            continue
        
        best_target = max(target_cols, key=lambda k: target_cols[k])
        best_score = target_cols[best_target]
        
        if best_score >= threshold and best_target not in used_target_cols:
            matches[source_col] = best_target
            used_target_cols.add(best_target)
    
    return matches

# ---------------------------------------------------------------
# Run the Matcher
# ---------------------------------------------------------------
column_matches = match_columns(snowflake_data, celonis_data, threshold=0.5)
print("Matched Columns (Snowflake → Celonis):")
print(column_matches)