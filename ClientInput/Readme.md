# Notes for ClientInput

This is where the agent will send its actions to have them actually executed. The library used expects to have the ```$DISPLAY``` environment variable set to the X display of the game running.

Actions should be sent as an array directly from the ```action_spec``` and this code will process that into actual keypresses and mouse movements.

---

## TODO

I haven't tested the speed of this library and need to benchmark it against others. For now it will work as a testing bed.
