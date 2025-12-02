import pandas as pd
import os

try:
    # Based on user output, the header is at row index 4
    print("Reading Excel file with header at row 4...")
    df = pd.read_excel('heritage_list.xls', header=4)
    
    # The column name is '명칭'
    target_col = '명칭'
    
    if target_col in df.columns:
        print(f"Found column: '{target_col}'")
        
        # Extract and clean names
        # Drop NaNs and get unique names
        names = df[target_col].dropna().unique().tolist()
        
        # Filter out any non-string items just in case
        names = [str(name).strip() for name in names if str(name).strip()]
        
        print(f"Extracted {len(names)} unique cultural heritage names.")
        
        # Limit to 2222 for testing (matching downloaded count)
        names = names[:2222]
        print(f"Limiting to first {len(names)} items for testing.")
        
        # Save to landmarks.txt
        output_file = 'landmarks.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for name in names:
                f.write(f"{name}\n")
                
        print(f"Successfully saved {len(names)} landmarks to '{output_file}'")
        print("You can now run 'download_images.py' and choose option 2.")
        
    else:
        print(f"Error: Column '{target_col}' not found. Available columns: {df.columns.tolist()}")

except Exception as e:
    print(f"Error processing file: {e}")
