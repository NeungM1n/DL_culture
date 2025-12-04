import pandas as pd

try:
    # Read Excel file
    df = pd.read_excel('backend/heritage_list.xls', header=4)
    
    # Check columns
    print("Columns:", df.columns.tolist())
    
    # Assuming '종목' is the column for type (National Treasure, etc.)
    # If not found, I'll print the first row to guess.
    if '종목' in df.columns:
        counts = df['종목'].value_counts()
        print("\n--- Heritage Counts by Type ---")
        print(counts)
        
        # Calculate cumulative sum to find cut-off for 1500
        print("\n--- Cumulative Counts ---")
        cumulative = 0
        for type_name, count in counts.items():
            cumulative += count
            print(f"{type_name}: {count} (Total: {cumulative})")
            
    else:
        print("'종목' column not found. First row data:")
        print(df.iloc[0])

except Exception as e:
    print(f"Error: {e}")
