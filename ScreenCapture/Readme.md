# Notes for Screen (state) capture.

### First, we create the virtual display:

```
LD_LIBRARY_PATH=/usr/lib/mesa-diverted/x86_64-linux-gnu Xvfb :99 +extension GLX -screen 0 640x480x24 & 
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
