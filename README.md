# User Sensor Data Generator App
### Python GUI app made with Tkinter library that generates fake data file of 1000 random sensor readings for each of 1000 random users, as well as provides data visualization tools to analyze the data generated.

Welcome to my fake data generator!
With the click of a button, generate fake data for 1000 random sensor readings for each of 1000 random users.

The generated user information includes: Firstname, Lastname, age, gender, username, address, email
The generated sensor readings include: Date, Time, Outside Temperature, Outside Humidity,  Room Temperature, Room Humidity

The instructions to set up and utitilize the program are:
1. Download iotapp.py file onto your local system.
2. To execute file, in Anaconda Prompt, locate directory where file was downloaded and enter script:
>>> python iotapp.py
3.  The file menu contains two sections: 'Create' and 'Statistics'

    Under 'Create', find options: 
        'Generate fake IoT user data', 
        'Save as JSON',
        'Save as CSV',
         and 'Exit'
         
    Under 'Statistics', find options: 
        'Plot A - histogram - outside temp',
        'Plot B - line graph - outside vs room temp',
        and 'Plot C - histogram - all data'
4. Enjoy!
