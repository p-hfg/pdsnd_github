import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months =  ['all','january','february','march','april','may','june']

days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = input("Which city you would like to analyse? Type 'Chicago', 'Washington' or 'New York City')  ").lower()
    while not(city in CITY_DATA.keys()):
        print('Invalid Input')
        city = input("Which city you would like to analyse? Type 'Chicago', 'Washington' or 'New York City')  ").lower()

    month = input("Enter any one of the first 6 months or enter All to select all 6 months. ").lower()
    while not(month in months):
        print('Invalid Input')
        month =input("Enter any one of the first 6 months or enter All to select all 6 months. ").lower()


    day = input("Enter any one of the days of the week or enter All to select all days. ").lower()
    while not(day in days):
        print('Invalid Input')
        dow = input("Enter any one of the days of the week or enter All to select all days. ").lower()

    print('-'*40)
    return city, month, day


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

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

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('the most common month is ',months[popular_month-1])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('the most common day is ',popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('the most common start hour is ',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('most commonly used start station is ',popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('most commonly used end station is ',popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trips']=df['Start Station']+' to '+df['End Station']
    print('most frequent combination of start station and end station trip is from ',df['trips'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = np.sum(df['Trip Duration'])
    print('the total travel time is ',total_time)

    # display mean travel time
    mean_time = np.mean(df['Trip Duration'])
    print('the mean travel time is ',mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users=df['User Type'].value_counts()
    print('the count for Subscriber is ',users['Subscriber'])
    print('the count for Customer is ',users['Customer'])

    # Display counts of gender
    if not('Gender' in df.columns):
        print('Sorry, but the system does not have data related to gender to this city')
    else:
        gender=df['Gender'].value_counts()
        print('the count for Males is ', gender['Male'])
        print('the count for Females is ', gender['Female'])


    # Display earliest, most recent, and most common year of birth
    if not('Birth Year' in df.columns):
        print('Sorry, but the system does not have data related to birth year to this city')
    else:
        print('the earliest year of birth is ', df['Birth Year'].min())
        print('most recent year of birth is ', df['Birth Year'].max())
        print('most common year of birth is ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """ Displays lines of individual trips data according to the user """

    i = 0
    raw = input("Would you like to see individual trip data? Type 'yes' or 'no'  ").lower()
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            df2 = df.drop(['month','day_of_week','hour','trips'],axis=1)
            print(df2[i:i+5])
            raw = input("Would you like to see  more individual trip data? Type 'yes' or 'no'  ").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nWould you like to restart? Type 'yes' or 'no'.\n").lower()
        valid_input = ['yes','no']
        while not(restart in valid_input):
            print('Invalid Input')
            restart = input("\nWould you like to restart? Type 'yes' or 'no'.\n").lower()
        if restart == 'no':
            break


if __name__ == "__main__":
	main()
