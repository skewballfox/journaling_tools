# Writing Tools

## Description

This is a collection of scripts, template files, and user services for my daily writing. my templates are in markdown because it's easy to convert to other formats and is faster to write for me. 


## Notes

At the moment only 3 of the templates are controlled via timers: the dream journal, the start of day notes, and the nightly journal. These files are organized in a directory structure via the date, as this seemed like the best practice for something I'm hoping to do on a daily basis. The timers and the services are user services, which means the creation doesn't require sudo permissions, and isn't going to affect other users.  

I changed the launcher to use a list rather than the templates directory for creating the daily files, it's less to change with the creation of each new file, and it's easier to read. 


if you need to see the keybinds or things not connected to this repository (such as environment variables), you can find those in my [repository](https://www.github.com/skewballfox/.cfg) containing my config files. 

## TODO

Find a way to syncronize between two computers with zero/extremely minimal data loss(empty file overwriting filled file, or a file getting filled with junk), planning on using drive

Implement some kind of tagging system

Build a scraper for weather data, while not related to the daily task, it is something that I feel should be used in within the larger context of self-tracking

perhaps build a relational database around keeping this and other self-tracking data organized. 

if possible, I would like to condense this down to one service which is passed variables to indicate the file name when launched by specified timers. This may not be in the realm of possibility or may take more effort than having damn near identical services per target.

may set the editor to use(with different commandline arguments) in an environment variable, as in leau of the above possiblity this would reduce the amount of changes you needed to make if you wanted to switch to a different editor/setup.

## Install 

If you use systemd all you need to do after downloading this repository is run the populate script. the systemd user services are set to use kakoune at the moment, but I've used them with both vscode and gxi. 