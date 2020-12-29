from tkinter import *
import json
import random 
from datetime import date, timedelta
import faker

import calendar
import numpy as np
from pandas import DataFrame
import arrow
import pandas as pd

def donothing(): #event placeholder
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def gen_data():
    fake = faker.Faker()
    #instantiate Faker
    usernames = set()
    usernames_no = 1000

    #populate the set with 1000 unique usernames
    while len(usernames) < usernames_no:
        usernames.add(fake.user_name())
        
    #loop for 1,000 elements
    def get_random_name_and_gender():
        skew = .6 # 60% of users will be female
        male = random.random() > skew
        if male:
            return fake.name_male(), 'M'
        else:
            return fake.name_female(), 'F'

    def get_users(usernames):
        users = []
        for username in usernames:
            name, gender = get_random_name_and_gender()
            user = {
                'username': username,
                'name': name,
                'gender': gender,
                'email': fake.email(),
                'age': fake.random_int(min=18, max=90),
                'address': fake.address()
            }
            users.append(json.dumps(user))
        return users

    #sensor records' date-time generation logic

    #yyyy-mm-dd_time format
    #remaining sensor inputs: Outside Temperature_Outside Humidity_Room     Temperature_Room Humidity

    def get_time():
        times = ['12:00am', '06:00am', '12:00pm', '06:00pm']
        return random.choice(times)

    def get_date():
        start = date.fromisoformat('2015-01-01')
        days_since_start = date.today() - start #range of days from 01-01-2015 to today
        duration = random.randint(1,days_since_start.days)
        offset = random.randint(-365, 365)
        day_being_assessed = date.today() - timedelta(days=duration)
        end = start + timedelta(days=duration)
        def _format_date(date_):
            return date_.strftime("%Y%m%d")
        return _format_date(end)

    def get_sensor_records_DATE_TIME():
        separator = '_'
        time_ = get_time()
        end = get_date()
        return separator.join(
            (time_, end))
    #6 collect all pieces and return final sensor records' date-time
    #sensor data
    #Outside Temperature, Outside Humidity,  Room Temperature, Room Humidity

    def get_sensor_records_DATA():
        time_date = get_sensor_records_DATE_TIME()
        outsidetemp = random.randint(70,96)
        outsidehum = random.randint(50,96)
        roomtemp = int(outsidetemp - random.randint(0,11))
        roomhum = int(outsidehum - random.randint(0,11))

        return {
            'time_yyyy-mm-dd': time_date,
            'outsidetemp': outsidetemp,
            'outsidehum': outsidehum,
            'roomtemp': roomtemp,
            'roomhum': roomhum
        }

    #put data together
    def get_data(users):
        data = []
        for user in users:
            readings = [get_sensor_records_DATA()
                        for _ in range(random.randint(0,1001))]
            data.append({'user': user, 'readings': readings})
        return data
    #Cleaning the data
    rough_data = get_data(users)  

    data = []
    for datum in rough_data:
        for reading in datum['readings']:
            reading.update({'user': datum['user']})
            data.append(reading)

    #write data
    with open('testdata.json', 'w') as stream:
        stream.write(json.dumps(data))
    #load data
    with open('testdata.json') as stream:
        data = json.loads(stream.read())   

    #create DataFrame
    global df 
    df = DataFrame(data)
    
    count_row = df.shape[0]

    #8 explode time_yyyy-mm-dd into components, create separate DataFrame for them
    def unpack_time_date(name):
        time_, end = name.split('_')
        end = arrow.get(end, 'YYYYMMDD').date()
        return time_, end

    sensor_data = df['time_yyyy-mm-dd'].apply(unpack_time_date)
    sensor_data_cols = [
        'Time', 'End']
    sensor_data_df = DataFrame(
        sensor_data.tolist(), columns=sensor_data_cols, index=df.index)

    #pass column's names
    df = df.join(sensor_data_df)

    #unpacking the user data
    def unpack_user_json(user):
        user = json.loads(user.strip())
        return [
            user['username'],
            user['email'],
            user['name'],
            user['gender'],
            user['age'],
            user['address']
        ]

    user_data = df['user'].apply(unpack_user_json)
    user_cols = [
        'username', 'email', 'name', 'gender', 'age', 'address']
    user_df = DataFrame(
    user_data.tolist(), columns=user_cols, index=df.index)

    #join
    df = df.join(user_df)

    #14 change to better columns
    better_columns = [    
        'time_yyyy-mm-dd', 'Outside Temp', 'Outside Hum',
        'Room Temp', 'Room Hum', 'User',
        'Time', 'Date', 'Username',
        'Email', 'Name', 'Gender',
        'Age', 'Address'
    ]
    df.columns = better_columns
     
def save_json():
    df.to_json('df.json')
            
def save_csv():
    df.to_csv('df.csv')

#styling
import matplotlib.pyplot as plt
plt.style.use(['classic', 'ggplot'])
import pylab
pylab.rcParams.update({'font.family' : 'serif'})

#Data visualization options

#Plot A - histogram - outside temp
def plot_a():
    df[['Outside Temp']].plot.hist();

#Plot B - line graph - outside vs room temp
def plot_b():
    df_date[['Outside Temp', 'Room Temp']].plot();
    
#Plot C - histogram - all data
def plot_c():
    df[['Room Temp', 'Outside Temp', 'Room Hum', "Outside Hum"]].plot.hist();

#----------        
root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Generate fake IoT user data", command=gen_data)
filemenu.add_command(label="Save as JSON", command=save_json)
filemenu.add_command(label="Save as CSV", command=save_csv)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Create", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)

editmenu.add_separator()

editmenu.add_command(label="Plot A - histogram - outside temp", command=plot_a)
editmenu.add_command(label="Plot B - line graph - outside vs room temp", command=plot_b)
editmenu.add_command(label="Plot C - histogram - all data", command=plot_c)


menubar.add_cascade(label="Statistics", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)


root.config(menu=menubar)
root.mainloop()