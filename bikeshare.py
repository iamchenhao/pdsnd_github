import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Define function to get and check user input
def input_check(input_message, expect_list):
    """Ask user to input a value and check the input."""
    while True:
        try:
            input_value = input(input_message).lower()
        except (ValueError, KeyboardInterrupt):
            print('An error occurred')
        if input_value in expect_list:
            print('You have chosen {}.\n'.format(input_value.title()))
            break
        else:
            print('Sorry, not an appropriate choice, please try again.\n')
            continue
    return input_value

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filter_scope - the scope of time filter (by month, day, both, or no filter)
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Set user input messages & expected input
    input_city_txt = 'Would you like to see data for Chicago, New York City, or Washington?'
    expect_city_input = ['chicago', 'new york city', 'washington']

    input_filter_scope_txt = 'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.'
    expect_filter_input = ['month', 'day', 'both', 'none']

    input_month_txt = 'Which month? "January", "February", "March", "April", "May", "June", or "All".'
    expect_month_input = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    input_day_txt = 'Which day? "Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday", or "All".'
    expect_day_input = ['monday', 'tuesday', 'wednesday', 'thursday', 'saturday', 'sunday', 'all']

    # Get user input the city and filter scope (filter by month, day, both, or not at all)
    city = input_check(input_city_txt, expect_city_input)
    filter_scope = input_check(input_filter_scope_txt, expect_filter_input)

    # Get user to specify the month & week of day for filter
    if filter_scope == 'none':
        month = 'all'
        day = 'all'
    elif filter_scope == 'both':
        month = input_check(input_month_txt, expect_month_input)
        day = input_check(input_day_txt, expect_day_input)
    elif filter_scope == 'month':
        month = input_check(input_month_txt, expect_month_input)
        day = 'all'
    elif filter_scope == 'day':
        month = 'all'
        day = input_check(input_day_txt, expect_day_input)

    #Return values
    print('-'*40)
    return city, month, day, filter_scope

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_count = df['month'].value_counts().max()
    print('Most Popular Month:', popular_month, '; Count: ', popular_month_count)

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day_count = df['day_of_week'].value_counts().max()
    print('Most Popular Day of Week:', popular_day, '; Count: ', popular_day_count)

    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df['hour'].value_counts().max()
    print('Most Popular Start Hour:', popular_hour, '; Count: ', popular_hour_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_station_count = df['Start Station'].value_counts().max()
    print('Most Popular Start Station:', start_station, '; Count: ', start_station_count)

    # Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    end_station_count = df['End Station'].value_counts().max()
    print('Most Popular End Station:', end_station, '; Count: ', end_station_count)

    # Display most frequent combination of start station and end station trip
    com_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    com_station_count = df.groupby(['Start Station', 'End Station']).size().max()
    print('Most Popular Combination of Start Station & End Station:')
    print('{} (Start Station); {} (End Station); Count: {}'.format(com_station[0], com_station[1], com_station_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_delta = datetime.timedelta(seconds = int(total_time))
    print('Total Travel Time (seconds):', total_time)
    print('Total Travel Time (dd, hh:mm:ss) :', str(total_time_delta))

    # Display mean travel time
    avg_time = df['Trip Duration'].mean()
    avg_time_delta = datetime.timedelta(seconds = int(avg_time))
    print('\nAverage Travel Time (seconds):', avg_time)
    print('Average Travel Time (hh:mm:ss):', str(avg_time_delta))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User Types')
    user_types = df['User Type'].value_counts().to_dict()
    for key, value in user_types.items():
        print('Number of {}: {}'.format(key, value))

    # Display counts of genders
    print('\nCounts of Genders')
    if city in ['chicago', 'new york city']:
        gender = df['Gender'].value_counts().to_dict()
        for key, value in gender.items():
            print('Number of {}: {}'.format(key, value))
    else:
        print('Sorry, your filtered DataFrame doesn\'t include information on user\'s gender.')

    # Display earliest, most recent, and most common year of birth
    print('\nStatistics on Year of Birth')
    if city in ['chicago', 'new york city']:
        earliest_yob = df['Birth Year'].min()
        most_recent_yob = df['Birth Year'].max()
        common_yob = df['Birth Year'].mode()[0]
        common_yob_count = df['Birth Year'].value_counts()[common_yob]

        print('Earliest Year of Birth: ', int(earliest_yob))
        print('Most Recent Year of Birth: ', int(most_recent_yob))
        print('Most Common Year of Birth: ', int(common_yob), '; Count:', common_yob_count)
    else:
        print('Sorry, your filtered DataFrame doesn\'t include data on user\'s year of birth.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw(df):
    """Print raw data if user specify so."""
    first_prompt = '\nWould you like to view individual trip data? Type\'yes\' or \'no\''
    subsequent_prompt = '\nWould you like to view more individual trip data? Type\'yes\' or \'no\''
    expected_list = ['yes', 'y', 'no', 'n']
    i = 0
    view_raw_input = input_check(first_prompt, expected_list)
    while True:
        if view_raw_input in ['no', 'n']:
            break
        if view_raw_input in ['yes', 'y']:
            print(df.iloc[i:i+5, :])
            i += 5
            view_raw_input = input_check(subsequent_prompt, expected_list)
            continue


def main():
    while True:
        city, month, day, filter_scope = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        view_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
