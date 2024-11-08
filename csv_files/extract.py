import pandas as pd

def preprocess_the_ila_data(ila_csv, output_csv):
    """
    Process the ILA data from the input CSV and save the 4th readings 
    for each 'bram_address' in the specified output location.
    
    Parameters:
    - ila_csv (str): Path to the input CSV file.
    - output_csv (str): Path to save the processed CSV file.
    """
    df = pd.read_csv(ila_csv)  # Load the CSV file

    # Ensure we have the columns "ila_data" and "bram_address" in the dataframe
    if 'ila_data[639:0]' in df.columns and 'bram_address[7:0]' in df.columns:
        # Drop rows with missing values in 'ila_data' or 'bram_address'
        df = df.dropna(subset=['ila_data[639:0]', 'bram_address[7:0]'])

        # Group by 'bram_address' and grab the 4th reading
        # Reset index to make 'bram_address' a column again
        # Use nth(3) to get the 4th entry (0-based index)
        filtered_df = df.groupby('bram_address[7:0]').nth(3).reset_index()

        # Check if we have any entries left after filtering
        if not filtered_df.empty:
            # Exclude the first row if needed
            filtered_df = filtered_df[1:]

            # Save the filtered data to the specified output CSV file
            filtered_df.to_csv(output_csv, index=False)
            print(f"ILA readings saved to '{output_csv}'")
        else:
            print("No 4th reading available for some or all bram addresses.")
    else:
        print("Required columns ('ila_data[639:0]' and 'bram_address[7:0]') not found in CSV.")

# Example usage
# input_csv_path = './input_data/ila_data.csv'  # Change to your input file path
# output_csv_path = './specified_output_directory/fourth_ila_readings.csv'  # Set your desired output file path
# preprocess_the_ila_data(input_csv_path, output_csv_path)
