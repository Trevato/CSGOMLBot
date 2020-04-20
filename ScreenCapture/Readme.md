# Notes for Screen (state) capture.

### This directory contains the files to gather observations for our agent.

First, it must launch the game.
So far, I have been able to use something like:

*Note: This is a work in progress.*

```
 export DISPLAY=:1
 Xvfb :1 -screen 0 1024x768x16 
 ```
 This creates a virtual display that steam can then run inside of:
 
 *Note: The command here will be expanded to directly launch CSGO.*
 
 ```
 DISPLAY=:1 steam
 ```
 
 Once we have the game running, we can launch our Gamestate server for gathering client data and we can launch our screen recording scripts.
