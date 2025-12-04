import pandas as pd
import os

try:
    # Based on user output, the header is at row index 4
    print("Reading Excel file with header at row 4...")
    df = pd.read_excel('backend/heritage_list.xls', header=4)
    
    # The column name is '명칭'
    # The column name is '명칭' and '종목'
    target_col = '명칭'
    type_col = '종목'
    
    if target_col in df.columns and type_col in df.columns:
        print(f"Found columns: '{target_col}', '{type_col}'")
        
        # Filter for Major Heritage Sites (Total ~1500 target)
        # Priority: 국보 (National Treasure) > 보물 (Treasure) > 사적 (Historic Site)
        major_types = ['국보', '보물', '사적']
        
        filtered_df = df[df[type_col].isin(major_types)]
        
        # Extract and clean names
        names = filtered_df[target_col].dropna().unique().tolist()
        
        # Filter out any non-string items just in case
        names = [str(name).strip() for name in names if str(name).strip()]
        
        print(f"Extracted {len(names)} major cultural heritage names (국보, 보물, 사적).")
        
        # Limit to 1500 as requested
        if len(names) > 1500:
            names = names[:1500]
            print(f"Limiting to top {len(names)} items.")
        
        # Add specific requests if missing
        special_requests = ['숭례문']
        for req in special_requests:
            if req not in names:
                names.insert(0, req) # Add to top
                print(f"Added special request: {req}")
        
        # Save to landmarks.txt
        output_file = 'landmarks.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for name in names:
                f.write(f"{name}\n")
                
        print(f"Successfully saved {len(names)} landmarks to '{output_file}'")

        
    else:
        print(f"Error: Column '{target_col}' not found. Available columns: {df.columns.tolist()}")

except Exception as e:
    print(f"Error processing file: {e}")
