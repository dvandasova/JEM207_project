import pandas as pd
# Internal Input: Function to read the internal file and extract data
def read_excel_to_df(file_path):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Check if the DataFrame has the correct number of columns and they are in the expected order
        expected_columns = ['code', 'date', 'event', 'city', 'venue', 'accom. Code', 'flight.Code', 'Standard Accommodation', 'Superior Accommodation', 'Luxurious Accommodation', 'Standard Price', 'Superior Price', 'Luxurious Price', 'Standard Rating', 'Superior Rating', 'Luxurious Rating', 'Min Price', 'Standard Price Total', 'Superior Price Total', 'Luxurious Price Total']
        if len(df.columns) != len(expected_columns) or not all(df.columns == expected_columns):
            # If columns do not match, raise an error
            raise ValueError("Error: Unexpected input form.")

        # Convert the 'date' column to datetime dtype
        df['date'] = pd.to_datetime(df['date'])

        # Return the DataFrame
        return df
    
    except ValueError as ve:
        print(ve)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
