import matplotlib.pyplot as plt
import seaborn as sns

def plot_accommodation_data(accommodation_data_1):
    accommodation_data_1.plot(kind='bar', figsize=(12, 6))
    plt.title('Mean Price of Accommodation Types Over Time')
    plt.ylabel('Mean Price')
    
    # Instead of dates on the x-axis, show the dates as strings
    plt.xticks(ticks=range(len(accommodation_data_1.index)), 
               labels=[date.strftime('%Y-%m-%d') for date in accommodation_data_1.index], 
               rotation=45)
    plt.show()

def plot_standard(event_df):
    plt.figure(figsize=(12, 6))
    sns.heatmap(event_df['Standard Price Total'], annot=False, cmap='coolwarm')
    plt.title('Mean Price of Standard Accommodation for Home and Away Teams')
    plt.show()

def plot_superior(event_df):
    plt.figure(figsize=(12, 6))
    sns.heatmap(event_df['Superior Price Total'], annot=False, cmap='coolwarm')
    plt.title('Mean Price of Superior Accommodation for Home and Away Teams')
    plt.show()

def plot_luxurious(event_df):
    plt.figure(figsize=(12, 6))
    sns.heatmap(event_df['Luxurious Price Total'], annot=False, cmap='coolwarm')
    plt.title('Mean Price of Luxurious Accommodation for Home and Away Teams')
    plt.show()
