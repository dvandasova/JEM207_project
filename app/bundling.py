import pandas as pd

def select_accommodation_bundles(booking_data_df):
    # Price classification
    low_percentile = booking_data_df['Price_numeric'].quantile(0.33)
    mid_percentile = booking_data_df['Price_numeric'].quantile(0.66)

    # Distance classification
    low_dist_quantile = booking_data_df['Distance'].quantile(0.33)
    mid_dist_quantile = booking_data_df['Distance'].quantile(0.66)

    # Define a function to calculate rating points
    def rating_points(rating):
        if rating < 7:
            return 1
        elif rating <= 8.5:
            return 2
        else:
            return 3

    # Define a function to calculate distance points
    def distance_points(dist):
        if dist <= low_dist_quantile:
            return 3
        elif dist <= mid_dist_quantile:
            return 2
        else:
            return 1

    # Assign points based on rating
    booking_data_df['Rating_Points'] = booking_data_df['Rating'].apply(rating_points)

    # Assign points based on distance
    booking_data_df['Distance_Points'] = booking_data_df['Distance'].apply(distance_points)

    # Calculate total points by summing Rating_Points and Distance_Points
    booking_data_df['Total_Points'] = booking_data_df['Rating_Points'] + booking_data_df['Distance_Points']

    # Sort the dataframe by Total_Points in descending order
    booking_data_df = booking_data_df.sort_values(by='Total_Points', ascending=False)

    # Safely select the three accommodations based on price
    luxurious_bundle = booking_data_df.loc[booking_data_df['Price_numeric'] > mid_percentile]
    superior_bundle = booking_data_df.loc[(booking_data_df['Price_numeric'] > low_percentile) & (booking_data_df['Price_numeric'] <= mid_percentile)]
    standard_bundle = booking_data_df.loc[booking_data_df['Price_numeric'] <= low_percentile]

    # Check if there's data for each category and return the best accommodation based on Total_Points
    if not luxurious_bundle.empty:
        luxurious_bundle = luxurious_bundle.iloc[0]
    else:
        luxurious_bundle = {'Name': 'Not Found', 'Price': 0, 'Rating': 0, 'Total_Points': 0}

    if not superior_bundle.empty:
        superior_bundle = superior_bundle.iloc[0]
    else:
        superior_bundle = {'Name': 'Not Found', 'Price': 0, 'Rating': 0, 'Total_Points': 0}

    if not standard_bundle.empty:
        standard_bundle = standard_bundle.iloc[0]
    else:
        standard_bundle = {'Name': 'Not Found', 'Price': 0, 'Rating': 0, 'Total_Points': 0}

    return standard_bundle, superior_bundle, luxurious_bundle
