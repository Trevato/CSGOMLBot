# Notes for Screen (state) capture.

### First, we start the game using an X display:

 ```
 xinit /root/.steam/steam.sh -applaunch 730 -gl
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

With the current setup, the game is running on the CPU. In the future, it may be beneficial to run in the GPU, or we can reserve that for training as the game runs fine.
