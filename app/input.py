import pandas as pd
# Internal Input: Function to read the internal file and extract data
def read_excel_to_df(file_path):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # Check if the DataFrame has the correct number of columns and they are in the expected order
        expected_columns = ['code', 'date', 'event', 'city', 'venue', 'accom.Code', 'flight.Code']
        if len(df.columns) != len(expected_columns) or not all(df.columns == expected_columns):
            # If columns do not match, raise an error
            raise ValueError("Error: Unexpected input form. Please insert a file containing " +
                             "\"code\", \"date\", \"event\", \"city\", \"venue\", \"accommodation code\" and \"flight code\" in this order.")

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

# User Input: Function to check code and return error message if correct input code not found
def check_code(primary_code, dataframe):
    # Extract first column of the dataframe
    codes = dataframe.iloc[:, 0:1]
    # Check if the primary code exists in the internal list of codes
    if primary_code in codes.values:
        pass
    else:
        print(f"Error: Code {primary_code} is not a valid input. Please check the code and try again.")
    # Check if the primary code corresponds to a date that is at least 2 weeks from today. Date is in second column of the data frame
    if dataframe.loc[dataframe.iloc[:, 0] == primary_code].iloc[0, 1] >= pd.Timestamp.today() + pd.DateOffset(weeks=2):
        pass
    else:
        print(f"Error: Code {primary_code} is not a valid input. The date corresponding to this code is less than 2 weeks from today. Please check the code and try again.")
    return

# User Input: Function to read the input file and extract data
def read_code(file_path, internal_list):
    with open(file_path, 'r') as file:
        file.readline()  # Skip the first line as it's not needed for the code
        primary_code = file.readline().strip()  # Read the second line for primary code

        # Check if the primary code exists in the internal list of codes
        check_code(primary_code, internal_list)
    
    return primary_code
