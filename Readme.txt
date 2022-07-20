First install the bridge to your server and put the IP address and the port in config.txt
then run the bridge

Copy client program to related end points and make it to run in startup (copy a shortcut of "URDClientService.exe" to C:\Users\**User**\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

Copy the Administrator file to admin computers and run administrator program

Add config.txt file to both Client and administrator directory

config.txt file should be like below - ServerIP- the IP of the machine that runs bridge program/ ServerPort- port that you have mentioned in servers' config.txt

ServerIP
ServerPort

all directories must have the same config.txt
