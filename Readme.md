# Daily Tasks

Routine is at the heart of productivity for me, so I created this as a way of enforcing it. If I leave it up to me, I struggle to do things like keep a journal, because often my it's hard to bring my attention away from what is right in front of me. This makes the habit easier to start and maintain. 

## Notes 
Right now all this does is launches a few journals that I intend to keep daily through VS Code at specified times using systemd timers. 

I used VS Code instead of Atom because of the command line interface

I used Systemd instead of Chron because I need to get better with it for some projects automating webscraping. slicing is super useful for resource management. 

I recently removed Tagging from both the dream journal and the evening journal, because tagging should be something that is automated. The way I look at it it's metadata, which is something I should be less concerned about directly. It's useful for analysis, but trying to write it manually is both cumbersome and error-prone. 

I removed weather, and places visited from the evening journal for similar reasons. it's metadata, and should be tracked by other methods. 

I removed emotions because trying to document them is tedious, and I need to get in the habit of using more emotional language. The goal is to be able to pick up what emotions I was experiencing through Analysis of the written parts.

## TODO

Find a way to syncronize between two computers with zero/extremely minimal data loss(empty file overwriting filled file, or a file getting filled with junk), planning on using drive

Implement some kind of tagging system

Build a scraper for weather data, while not related to the daily task, it is something that I feel should be used in within the larger context of self-tracking

perhaps build a relational database around keeping this and other self-tracking data organized. 

## Install 
If you use systemd all you need to do after downloading this repository is run the populate script with sudo permissions. 