# EFT_MAP_RADAR
Needs a few packages: flask, flask_socketio

Run main.py, connect to 127.0.0.1:8080. May want to turn on logging or flask debugging if you are troubleshooting. 


What is it:
This is a web browser radar based off a C# radar. All backend data is used from this project: https://github.com/Mischahe/eft-dma-radar-1 which I have tweaked and updated to allow data to be passed to python via JSON and pushed to python flask which will reveal a radar in real time, similar to the C# but with a few changes since its using html canvas and can be used with multiple people.

How it runs:
Grabs jsons files from C:\json_data\ reads this file,
parses it to lists and then sends it to flask. Flask then reads it in
with the threading events and sends it off to javascript. Javascript then
reads each list and uses html canvas to create the dots which represent the 
characters and objects in the game.

I have added a sample folder which has the json data that it would normally get from EFT and place it in C:\json_data. You can use this to test if your changes are working. 

WARNING: I would not host this public. There hasn't been any testing for vulnerabilities which i'm sure there is. 

