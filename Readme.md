# Writing Tools

## Description

This is a set of tools for automating the creation of journals and notes based off templates. The best way to make a habit of something is to make it easy. 

It currently supports keyword replacement in both the naming of the file and the file itself. It uses systemd at user level to launch the journals at specified times. 

The directory structure of the journal is something like a time based cache. I primarily use ranger to view my files and traverse my directories, so I like tend to like trees. the files are sorted by creation date into 5 different directories, this week, last week, this quarter, this year, and everything else. 


## Notes

This is mainly meant for personal use, but if this seems like something you want to use or add to feel free. I do plan on adding things like document tagging later on and keyword insertion based on the output of certain commands(make it easier to view things like history), among other things. but no idea when I'll pick up working on this project again. 


## Install 

The python code uses modules from the standard library and nothing else, so it should work out of the box

If you use systemd all you need to do after downloading this repository is run the populate script. 
the systemd user services are set to use kakoune at the moment, but I've used them with both vscode and gxi. 
Depending on your DE and how you launch your graphical session, systemd user services may or may not have access to the display environment, if you have a minimal install, you may want to 
append `systemctl --user import-environment DISPLAY` to whatever you use to lauch your xsession. 

