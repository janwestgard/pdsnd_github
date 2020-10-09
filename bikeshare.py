import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
   
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    #Variables used for input from user
    city = 'city'
    month = 'month'
    day = 'day'
   
    print('\nHello! Let\'s explore some US bikeshare data!')
    #Get user input for city (chicago, new york city, washington)

    while city not in ('chicago', 'new york city', 'washington'):
        city = input("Would you like to explore chicago, new york city or washington?\n\n").lower()

    # Get user input for month (all, january, february, ... , june)
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input("Would you like to explore data from january, february, march, april, may, june or 'all'?\n\n").lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ('all', '0', '1', '2', '3', '4', '5', '6'):
        day = input("Which day of the week would you like to get data from (enter a number from 0 to 6 where 0 is sunday, 1 is monday... or 'all'?\n\n").lower()
    
    print('-'*40)
    return(city, month, day)


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    return(df)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month:', most_common_month)

    # Displays the most common day of week
    most_common_day = df['day'].mode()[0]
    print('Most common day of week:', most_common_day)
    
    # Displays the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common start hour:', most_common_hour)
    
    # Displays the time for calculating rounded to 5 digits
    print("\nThis took %s seconds." % round((time.time() - start_time), ndigits=5))
    print('-'*40)
    return(df)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_commonly_start_station = df['Start Station'].mode()[0]
    print('Most commonly start station:', most_commonly_start_station)

    # Display most commonly used end station
    most_commonly_end_station = df['End Station'].mode()[0]
    print('Most commonly end station:', most_commonly_end_station)

    # Display most frequent combination of start station and end station trip 
    most_frequent_combination_stations = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent combination of start station and end station trip:', most_frequent_combination_stations)

    # Displays the time for calculating rounded to 5 digits
    print("\nThis took %s seconds." % round((time.time() - start_time), ndigits=5))
    print('-'*40)
    return(df)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time)

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    # Displays the time for calculating rounded to 5 digits
    print("\nThis took %s seconds." % round((time.time() - start_time), ndigits=5))
    print('-'*40)
    return(df)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nThe counts of Gender:\n', gender)
    else:
        print('\nGender is not available in the dataset')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        print('\nThe oldest customer is born in the year:', earliest_birth)

        most_recent_birth = int(df['Birth Year'].max())
        print('The youngest customer is born in the year:', most_recent_birth)

        most_common_year_of_birth = int(df['Birth Year'].mode()[0])
        print('Most common year of birth:', most_common_year_of_birth)
    else:
        print('\nBirth date is not available in the dataset')

    # Displays the time for calculating rounded to 5 digits
    print("\nThis took %s seconds." % round((time.time() - start_time), ndigits=5))
    print('-'*40)
    return(df)

#Ask if the user want to see the raw data (first five rows)
def user_data(df):
    """Displays raw data if the user want to see this"""
    raw_data = input('\nType yes if you would like to see the raw data from the file?\n').lower()
    n = 0
    
    while raw_data == 'yes':
        print(df.iloc[n:(n+5)])
        n += 7
        raw_data = input('\nDo you like to see five more rows, type yes?\n').lower()
    return()
        
# Main function calls for user input and runs the program until user ask's to quit
def main():
    # The program loops until user choose someting else than 'yes'
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        user_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# Starts the program by calling main
main()



