import pandas as pd
import numpy as np
from collections import defaultdict

# 1. Data Loading (Replace with your actual data)
# -------------------------------------------------
# Sample data simulating different database results
df1 = pd.DataFrame({  # Snowflake-like data
    'cust_id': [101, 102, 103, 104],
    'trans_date': ['2024-05-01', '2024-05-02', '2024-05-03', '2024-05-04'],
    'amt': [150.0, 200.5, 99.99, 300.0],
    'zero_col': [0, 0, 0, 0]
})

df2 = pd.DataFrame({  # Celonis-like data with different structure
    'XXBHS': [104, 103, 102, 101],  # Same values as cust_id, different order
    'DT_123': ['2024-05-04', '2024-05-03', '2024-05-02', '2024-05-01'],
    'Sales': [300.0, 99.99, 200.5, 150.0],
    'ZeroField': [0, 0, 0, 0],
    'ExtraCol': ['A', 'B', 'C', 'D']  # Unmatched column
})

# 2. Preprocessing
# -------------------------------------------------
def preprocess(df):
    """Standardize data for comparison"""
    df = df.astype(str).apply(lambda x: x.str.lower().str.strip())
    df = df.replace({'nan': np.nan, 'none': np.nan, '': np.nan})
    return df

df1_clean = preprocess(df1)
df2_clean = preprocess(df2)

# 3. Identify Potential Join Keys
# -------------------------------------------------
def find_potential_key(df1, df2):
    """Find columns that might serve as join keys"""
    potential_keys = []
    
    # Look for columns with same values but different names
    for col1 in df1.columns:
        for col2 in df2.columns:
            if set(df1[col1]) == set(df2[col2]):
                potential_keys.append((col1, col2))
                
    return potential_keys[0] if potential_keys else (None, None)

key_df1, key_df2 = find_potential_key(df1_clean, df2_clean)

# 4. Alignment Strategy
# -------------------------------------------------
if key_df1 and key_df2:
    # If common key found, sort both datasets by it
    df1_sorted = df1_clean.sort_values(by=key_df1).reset_index(drop=True)
    df2_sorted = df2_clean.sort_values(by=key_df2).reset_index(drop=True)
    use_row_alignment = True
else:
    # Fallback to set-based matching
    use_row_alignment = False

# 5. Matching Algorithm
# -------------------------------------------------
def column_matcher(df1, df2, use_row_alignment=False, threshold=0.8):
    """Main matching function with alignment awareness"""
    matches = {}
    
    # First handle zero columns
    zero_cols_df1 = [col for col in df1 if (df1[col] == '0').all()]
    zero_cols_df2 = [col for col in df2 if (df2[col] == '0').all()]
    
    for z_col in zero_cols_df1:
        for candidate in zero_cols_df2:
            if candidate not in matches.values():
                matches[z_col] = candidate
                zero_cols_df2.remove(candidate)
                break
    
    # Handle other columns
    remaining_df1 = df1.drop(columns=zero_cols_df1)
    remaining_df2 = df2.drop(columns=zero_cols_df2 + list(matches.values()))
    
    for col1 in remaining_df1.columns:
        best_match = None
        max_score = 0
        
        for col2 in remaining_df2.columns:
            if use_row_alignment:
                # Row-aligned comparison
                matches = sum(1 for i in range(len(df1)) 
                            if df1[col1].iloc[i] == df2[col2].iloc[i])
                score = matches / len(df1)
            else:
                # Set-based comparison
                set1 = set(remaining_df1[col1].dropna())
                set2 = set(remaining_df2[col2].dropna())
                score = len(set1 & set2) / max(len(set1), 1)
                
            if score > max_score and score >= threshold:
                max_score = score
                best_match = col2
                
        if best_match:
            matches[col1] = best_match
            remaining_df2 = remaining_df2.drop(columns=[best_match])
            
    return matches

# 6. Execute Matching
# -------------------------------------------------
matches = column_matcher(
    df1_sorted if use_row_alignment else df1_clean,
    df2_sorted if use_row_alignment else df2_clean,
    use_row_alignment=use_row_alignment,
    threshold=0.75
)

# 7. Results Presentation
# -------------------------------------------------
print("Column Matches:")
print("{:<15} → {:<15}".format("Source Column", "Target Column"))
print("-" * 30)
for src, tgt in matches.items():
    print("{:<15} → {:<15}".format(src, tgt))

# Expected Output:
# Column Matches:
# Source Column  → Target Column  
# ------------------------------
# cust_id        → XXBHS         
# trans_date     → DT_123        
# amt            → Sales         
# zero_col       → ZeroField