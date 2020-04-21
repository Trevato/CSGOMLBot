# Notes for Screen (state) capture.
*So far I am able to run simulations inside of the virtual display. Next we need to launch CSGO inside of it.*

### First, we create the virtual display:

This starts a virtual display named :1 with the GLX extension.

```
LD_LIBRARY_PATH=/usr/lib/mesa-diverted/x86_64-linux-gnu Xvfb :99 +extension GLX -screen 0 640x480x24 & 
 ```
 
### Then, we need to run something on that dislay:
 
 *Note: This is a simulation. Hopefully CSGO will run in a similar fashion.*
 
 ```
LD_LIBRARY_PATH=/usr/lib/mesa-diverted/x86_64-linux-gnu DISPLAY=:99 glxgears
 ```
 
 Now, I am successfully able to launch steam and in turn, launch CSGO using the graphical interface:
 
 ```
 LD_LIBRARY_PATH=/usr/lib/mesa-diverted/x86_64-linux-gnu DISPLAY=:1 /path/to/script/steam.sh
 ```
 
### Lastly, we can view what it looks like for testing purposes:
 
 In order to view what the virtual display is showing, we can connect to the server with VNC by referring to [this](https://www.howopensource.com/2014/10/connect-to-linux-desktop-from-windows/) and using this command:
 ```
 sudo x11vnc -safer -localhost -nopw -once -display :1 -auth /var/run/slim.auth
 ```
