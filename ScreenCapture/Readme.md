# Notes for Screen (state) capture.

*See bottom for notes for a fresh server.*

### First, we start the game using an X display:

*This launches directly into a deathmatch game on de_dust.*

 ```
 xinit /root/.steam/steam.sh -applaunch 730 -gl +map de_dust +cl_showfps 1 +sv_lan 1 -nointro +game_mode 2 +game_type 1 +exec gamemode_deathmatch
 ```
 
### Then, we can view what it looks like for testing purposes:
 
 Log-in to Steam on any other computer and it will be just like another PC to stream from.

 Using the ```numpy_mss.py``` script, we can test the screenshot speed.

---
## Some Stats:

So far, in my minimal testing, I have been able to take a screenshot, and convert it to a numpy array at an absurdly fast rate. (Note: the game is running in a very small window ATM.)

Example:

```
root@TrevorServerDebian:/home/trevor/CSGOMLBot/ScreenCapture# python3 numpy_mss.py
Enter mode:fast
fps: 380.81568912293443
fps: 92.98771782024565
fps: 657.414420062696
fps: 942.7520791189031
fps: 682.4445167588675
fps: 898.9078439777111
fps: 679.7899513776337
fps: 870.5487754254877
fps: 682.6666666666666
fps: 910.4197959626655
```

---
## TO-DO:

Either render the game in a smaller frame or scale it down to mach the ```observation_spec```.

The game runs on the GPU right now. That will probably hurt training performance but not sure yet. Also, I need to see if installing CUDA drivers will start to break things.

# Notes for a fresh server (AWS)

### Install steam with required drivers etc.

```
sudo apt install git -y
git clone https://github.com/ShadowApex/steamos-ubuntu.git
cd steamos-ubuntu
sudo ./install.sh
```

### Install xinit to handle X server

```
sudo apt install xinit
```
