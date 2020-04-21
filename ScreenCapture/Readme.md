# Notes for Screen (state) capture.

### First, we create the virtual display:

```
LD_LIBRARY_PATH=/usr/lib/mesa-diverted/x86_64-linux-gnu Xvfb :1 +extension GLX -screen 0 640x480x24 & 
 ```
 
### Then, we need to run CSGO on that dislay:
 
 ```
 LD_LIBRARY_PATH=/usr/lib/mesa-diverted/x86_64-linux-gnu DISPLAY=:1 /path/to/script/steam.sh -applaunch 730
 ```
 
### Lastly, we can view what it looks like for testing purposes:
 
 In order to view what the virtual display is showing, we can connect to the server with VNC by referring to [this](https://www.howopensource.com/2014/10/connect-to-linux-desktop-from-windows/) and using this command:
 ```
 sudo x11vnc -safer -localhost -nopw -once -display :1 -auth /var/run/slim.auth
 ```

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

With the current setup, the game is running on the CPU. In the future, it may be beneficial to run in the GPU, or we can reserve that for training as the game runs fine.
