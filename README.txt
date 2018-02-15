Client exerciser is a Python-Selenium based utility for iterating thru and check that the sheets in a defined set of
qvw applications are loaded properly in the AJAX client.

It is built using Python 3.6 and Selenium 2.0.
For the latest runtimes, check https://www.python.org and http://www.seleniumhq.org
(After installing Python from the website, the easiest way to get the latest Selenium version is to run the command
 "pip install selenium")

 To prepare the project for running, you need to provide some configuration information.
 The config.json holds general information for the project:

{
    "LogFile": "C:/PageStatus/QvwCheckLog.txt", -- This is the folder and filename where you want to keep the log
    "ScreenDump": "C:/PageStatus/", --This is the location for the temporary image file that is included in the error email
    "email": "someone@somewhere.com", --The email address to which the error email are sent
    "SystemName": "SomeSystem"
}

...to be completed...