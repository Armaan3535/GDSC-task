# GDSC-task
1) Adding a discord bot to your server using the discord developer portal
2) Getting the bot token and saving it in an env file to use later
3) giving the bot the permissions 
4) installing the discord library and the genai library and importing them
5) getting the gemini api key and saving it in the env file
6) loading the env files to access the tokens and creating an event for when the bot logs into the server(reminder check here)
7) making the bot commands requiring a prefix(!)
8) writing the code so the bot doesnt reply to itself and replies only when it is mentioned
9) adding the gemini api so it responds to user messages
10) making a reminder system where it takes the number of seconds and the reminder name and reminds when the timer is over(!remindme)
11) being able to see the active reminders(!reminders_list)
12) !cancelreminder for cancelling the reminders - FIXED
13) also deletes the reminder when it is over
14) creating a poll system where it takes the question and the options to make a poll on discord
15) !poll - FIXED
16) member join feature(whenever a new member joins it welcomes on the channel named welcome) FIXED
17) Added the Configurations to the gemini api and giving it a prompt for how I want it to act


-----------bugs fixed ----------
for !poll, made the argument optional so if it has a None value it tells you the format you should be using, it does the same if you only gave an input with the question and no options

for !cancelreminder i was using another filtered list to remove the reminders from instead i used the original list and removed the reminders from that

the member join function was not working because the member intent wasnt turned on in the discord developer portal and in the code too.


---- all features-----
respods to user messages using the Gemini API
Can create and delete reminders and also see the list of reminders(!remindme , !cancelreminder , !reminders_list)
can create polls (!poll Question?a;b;c)
The bot welcomes new members in the 'welcome' channel


--------things left to add if time is there--------
!help (learning how to change the help section and making it more cleaner)
music queue system (no idea how to do that but would learn if given more time)
maybe add more configurations to the gemini API and learning more about it

