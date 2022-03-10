# US BIKESHARE Project
# CREATED & submitted By Andre PORTE
# January 10th 2022

#Functions summary
# get_filters()
# load_data(city, month, day)
# time_stats(df)
# station_stats(df)
# trip_duration_stats(df)
# user_stats(df)
# main()


import time
import pandas as pd
import numpy as np

#Define global variables

CITIES_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
months = ['all','january','february', 'march', 'april', 'may', 'june']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
#reminder : weekday function : Monday = 0, Sunday = 6


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWhich city do you want to analyse ?\n')
    while city.lower() not in CITIES_DATA:
        city = city_error(city)
        print(str(city))

    print('OK, we will analyse ' + city.capitalize())

    # get user input for month (all, january, february, ... , june)
    
    month = input('\nWhich month do you want to analyse ? (January to June, All, if you want full analysis)\n')
    while month.lower() not in months:
        month=input('Sorry, we have only the data for the first semester,\n please adjust your choice:')

    print("OK, let's analyse "+str(month) )

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('\nWhich day of the week do you want to analyse ? (All, if you want full analysis)\n')
    while day.lower() not in days:
        day=input('OOPS,check what you have type\n please adjust your choice:')

    print("OK, let's analyse "+str(day) )       
    print('To summarize, we will analyse the data for {} during {} Month {}'.format(city,month,day))

    print('-'*40)
    return city, month, day

def city_error(city):
    city = input(str(city)+' is not available, please choose Chicago, New York City or Wahington : ')
    return city


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
    #load the CSV file by searching the filename in the dictionnary
    df = pd.read_csv(CITIES_DATA[city.lower()])

    #convert string to date time format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour']=df['Start Time'].dt.hour

    #filter the dataframe
    if month.lower() != 'all':
        month = months.index(month.lower())
        #filtre sur l'index
        df = df[df['Month']==month]

    #filtre sur le jour de la semaine
    if day.lower() != 'all':
        day = days.index(day.lower())
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month=df['Month'].mode()[0]
    print('Most popular Month : {}'.format(months[popular_month]))

    # display the most common day of week
    popular_day=df['day_of_week'].mode()[0]
    print('Most popular day   : {}'.format(days[popular_day]))

    # display the most common start hour
    popular_hour=df['hour'].mode()[0]
    print('Most popular Hour  : {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mcu_startst = df['Start Station'].mode()[0]
    print('Most Common Start Station : {}'.format(mcu_startst))

    # display most commonly used end station
    mcu_endst = df['End Station'].mode()[0]
    print('Most Common End  Station : {}'.format(mcu_endst))

    # display most frequent combination of start station and end station trip
    mcu_combst = (df['Start Station']+' - '+df['End Station']).mode()[0]
    print('Most Common combined Station : {}'.format(mcu_combst))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('Total travel time   = {}'.format(total_travel_time))

    # display mean travel time
    avg_travel_time=df['Trip Duration'].mean()
    print('Average travel time = {}'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    nb_users = df['User Type'].nunique()
    st_users = df.groupby(['User Type']).size()
    print('nb of user type = {}'.format(nb_users))

    # Display counts of gender
    try:
        st_gender = df.groupby(['Gender']).size()
        #print('nb of Gender = {}'.format(st_gender))
    except KeyError:
        print('sorry, we don''t have any data for gender analyse')
    else:
        print('nb of Gender = {}'.format(st_gender))

    # Display earliest, most recent, and most common year of birth
    try:
        birth_earliest = df['Birth Year'].min()
    except:
        print('Sorry, no birthadate available for analysis')
    else:
        birth_mostrecent = df['Birth Year'].max()
        birth_mostcomyear = df['Birth Year'].mode(dropna=True)[0]
        print('Birth Year \n Earliest : {}\n Most Recent : {}\n Most Common : {}'.format(birth_earliest,birth_mostrecent,birth_mostcomyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        counter = 0
        viewraw = input('do you want to see the raw data ? (Yes or No)')
        while viewraw.lower() == 'yes':
            print(df.iloc[counter:counter+5])
            counter += 5
            viewraw = input('do you want to see more raw datas ? (Yes or No)').lower()
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


