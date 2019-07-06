# speed_checker_tool

A tool for internet provider technicians so they can
provide a comparison of the internet connection versus the average
for given location.

Setup

from tool ROOT execute command:
    
    pip install -r requirements.txt

to run execute command:

    python broadband_compare.py  args


Features

Currently the tool will take a specified user location and then output the average download speed
of the user specified location and return the average speed of the country as well as the location.

The user can also specify a location to compare the specified user location to another.


Design choices
The tool relies on using sqlite simply for ease of accessing data after converting to sql from pandas.

I've endeavoured to keep the tool simple initially as an MVP. However, there is scope to increase the complexity
by adding functionality to create charts using PyChart. This feature would output the results of the user specified
speed against a barchart / scatter graph to indicate in a more visual way how the broadband speed compares.

I have elected to only represent a small amount of the data but the tool allows for easy feature addition.



