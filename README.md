# ServiceReStarter
The SRS is a tool to start or stop services on a windows machine. The services
to be restarted can be manually given in a txt file.

## Generation of exe file
To start or stop services, administrator privileges are required. To get these
(and for convenience) the python script can be converted to an exe file using

` pyinstaller --onefile servicerestarter.exe`

This needs to be done only once. The txt file is read on every program launch.

### Improvements
For some reasons the -w parameter of pyinstaller does not work as expected.
Therefore the console window is present. This might be due to the application
loop in wx. Someday in version 2.0 this might get fixed.

## services.txt
In the services.txt_sample there are samples for services. The first value in
a tuple states the service name, the second value holds the display name.

## color coding
There are three possible colors of services in the window:

- green: the service is running
- red: the service is stopped
- grey (and inactive): there was a problem finding the service

Sorry to the color blind out there. This is only a first version and colors
might be replaced with images.