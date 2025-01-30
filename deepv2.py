import pandas as pd
from collections import defaultdict

# Sample data (replace with your actual data)
df1 = pd.DataFrame({
    'CustomerID': [101, 102, 103],
    'Revenue': [500, 600, 700],
    'OrderDate': ['2024-05-01', '2024-05-01', '2024-05-01'],
    'UnmatchedColumn': [1, 2, 3]  # Example column with no match in df2
})

df2 = pd.DataFrame({
    'XXBHS': [101, 102, 103],       # Matches CustomerID
    'Sales': [500, 600, 700],       # Matches Revenue
    'DT_123': ['2024-05-01', '2024-05-01', '2024-05-01']  # Matches OrderDate
})

# ---------------------------------------------------------------
# Matching Logic
# ---------------------------------------------------------------
def match_columns(source_df, target_df, threshold=0.5):
    # Initialize all source columns as "not found"
    matches = {col: "not found" for col in source_df.columns}
    used_target_cols = set()
    
    # Track scores: {source_col: {target_col: match_score}}
    score_matrix = defaultdict(dict)
    
    # Calculate overlap scores for all source-target pairs
    for source_col in source_df.columns:
        source_values = source_df[source_col].dropna().astype(str).tolist()
        
        for target_col in target_df.columns:
            target_values = target_df[target_col].dropna().astype(str).tolist()
            
            # Calculate value overlap percentage
            overlap = len(set(source_values) & set(target_values))
            total = max(len(source_values), 1)  # Avoid division by zero
            score = overlap / total
            
            score_matrix[source_col][target_col] = score
    
    # Prioritize source columns with the highest best-score first
    sorted_source_cols = sorted(
        source_df.columns,
        key=lambda col: max(score_matrix[col].values(), default=0),
        reverse=True
    )
    
    # Assign best matches (1:1 mapping)
    for source_col in sorted_source_cols:
        target_scores = score_matrix[source_col]
        if not target_scores:
            continue  # No possible matches
        
        # Find the best unmatched target column
        best_target = None
        best_score = 0
        for target_col, score in target_scores.items():
            if target_col not in used_target_cols and score > best_score:
                best_score = score
                best_target = target_col
        
        # Update matches if threshold is met
        if best_target and best_score >= threshold:
            matches[source_col] = best_target
            used_target_cols.add(best_target)
    
    return matches

# ---------------------------------------------------------------
# Run the Matcher
# ---------------------------------------------------------------
column_matches = match_columns(df1, df2, threshold=0.5)

print("Matched Columns (df1 → df2):")
for source_col, target_col in column_matches.items():
    print(f"{source_col} → {target_col}")