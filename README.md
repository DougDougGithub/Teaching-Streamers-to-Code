SETTING UP THE PROJECT:    

# Installing Python
https://www.python.org/downloads/release/python-392/    
Download the "Windows installer (64-bit)" version    
When you run the installer, be sure to check "Add to Path" button

# Install VSCode
Download: https://code.visualstudio.com/    
Hit next    
Browse for extensions    
Download the Python extension

# Twitch Moderation Auth Key
Go to https://twitchtokengenerator.com/    
Click Custom Scope Token    
Enable the following:     
chat:read    
chat:edit    
channel:moderate    
channel:read:subscriptions    
moderation:read    
moderator:manage:banned_users    
Then hit Generate Token! at the bottom    
Save the Access Key

# OpenAI API Key
Create an OpenAI Account    
Go to Billing section, add $5 to balance    
Set up API key

# Create Auth key env variables
Hit windows key, look for "Edit the system environment variables"    
Press Environment Variables    
In "User Variables..." window, hit new:    
Name: TWITCH_MOD_ACCESS_TOKEN    
Value: (copied key)    
Name: OPENAI_API_KEY    
Value: (copied key)    

# OBS Websockets setup
In OBS, click Tools -> WebSocket Server Settings    
Make sure “Enable WebSocket server” is checked     
Set Server Port as 4455    
Set Server Password as TwitchChat9

# OBS new sources (e.g. text elements)
Create a new Text GDI(+) source    
Name it "BANNED USER"

# Download this project's files
Dropbox link

# Pip install python modules
Open the window with the project files above    
Click in the folder address bar, type cmd, hit enter     
In the terminal, run "pip install -r requirements.txt"    

# Quest test run
Make sure that they can run level_0_code in their VSCode
