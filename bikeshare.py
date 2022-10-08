import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'new york' : 'new_york_city.csv',
              'washington': 'washington.csv' }

month_vals = ['all', 'january', 'february','march', 'april','may','june']
day_vals=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input to select city (chicago, new york city, washington):
    while True :

        citychoice=input('\nEnter city required (Chicago, New York City or Washington) ').lower()

        if citychoice in CITY_DATA:
            city=citychoice
            break
        else:
            print('\nInvalid city! Please try again: \n')

    city=CITY_DATA[city]

    # Get user input to select month (all, january, february, ... , june):
    while True :

        monthchoice=input('\nEnter month required (type the name of the month (between Jan and June), or type \'all\' to use all months) ').lower()

        if monthchoice in month_vals:
            month=monthchoice
            break
        else:
            print('\nInvalid month choice, please try again \n')


    # Get user input for day of week (all, monday, tuesday, ... sunday):
    while True :

        daychoice=input('Enter day of the week required (type the name of the day, or type \'all\' to use all days) ').lower()

        if daychoice in day_vals:
            day=daychoice
            break
        else:
            print('\nInvalid day choice, please try again \n')

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df[:]['Start Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour']=df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_num = month_vals.index(month)

        # filter by month to create the new dataframe
        df = df[df['month']==month_num]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_num = day_vals.index(day)-1  #indexed with Monday as 0, Tuesday as 1 etc
        df = df[df['day_of_week']==day_num]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        month_mode=int(df['month'].mode())
        month_mode_label=month_vals[month_mode]
        print('\nThe most popular month to travel in was {}'.format(month_mode_label.title()))
    else:
        print('\nEvaluating data for {} only, as requested'.format(month.title()))

    # display the most common day of week
    if day == 'all':
        day_mode=int(df['day_of_week'].mode())
        day_mode_label=day_vals[day_mode+1]
        print('\nThe most popular day to travel on was {}'.format(day_mode_label.title()))
    else:
        print('\nEvaluating data for {} only, as requested'.format(day.title()))

    # display the most common start hour
    hour_mode=int(df['hour'].mode())
    print("The most popular hour to start a journey was", hour_mode, ':00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    st_st=df['Start Station'].mode()
    print('The most commonly used start station was {}'.format(st_st[0]))

    # display most commonly used end station
    en_st=df['End Station'].mode()
    print('The most commonly used end station was {}'.format(en_st[0]))

    # display most frequent combination of start station and end station trip
    station_combo=df['Start Station'] + ' to ' + df['End Station']
    print('\nThe most frequent combination of start and end station was', station_combo.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum() / 3600
    print('The total travel time accross all journeys was ', int(total_travel_time), 'hours')

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('\nThe mean travel time was' ,int(mean_travel_time) ,'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if city != 'washington.csv':


        # Display counts of user types
        users=df['User Type'].value_counts()
        user_dict=users.to_dict()
        print('\nThe number of users by type is as follows:')
        for key,val in user_dict.items():
            print(key , ':' , val)

        # Display counts of gender
        print('\nThe total number of users by gender is: ')
        genders=df['Gender'].value_counts()
        gender_dict=genders.to_dict()
        for key,val in gender_dict.items():
            print(key , ':' , val)


        # Display earliest, most recent, and most common year of birth
        print('\nThe earliest user date of birth is:', int(df['Birth Year'].min()))
        print('\nThe most recent user date of birth is:', int(df['Birth Year'].max()))
        print('\nThe most common user date of birth is:', int(df['Birth Year'].mode()))
    else:
        print('\nNo user information available for the city of Washington')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_data(df):
    """Displays raw data, 5 rows at a time. """
    keep_going = True    #variables to control the loop printing the raw data
    ind=0

    while keep_going == True:
        for i in range(5):
            row_dict=df.iloc[ind+i].to_dict()  #print 5 rows of the data
            for key , val in row_dict.items():
                print(key ,':', val)

            print('\n')
        ind+=5     #move on to the next block of data
        carry_on=input('Would you like to see 5 more entries? y\n')

        if carry_on != 'y':
            keep_going = False


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day) #display stats on journey times
        station_stats(df)          #display stats on stations
        trip_duration_stats(df)    #display stats on journey lengths
        user_stats(df, city)       #display stats about users

        # Show the user raw data in 5 row chunks, if required
        rawdat=input('\nWould you like to view example raw data? y or n ')

        if rawdat.lower() == 'y':
              show_data(df)


        # ask if the user would like to run another query
        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if (restart.lower() != 'yes' and restart.lower() != 'y'):
            break


if __name__ == "__main__":
	main()
