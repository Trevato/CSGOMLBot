# Notes for ClientInput

This is where the agent will send its actions to have them actually executed.

Actions should be sent as an array directly from the ```action_spec``` and this code will process that into actual keypresses and mouse movements.

*Unfortunatly the* ```action_spec``` *cannot be an array with recent tf updates and must be a discrete value. Will hopefully find the correct way to do this soon.*

---

## TODO

- Mouse movements using [this library](https://github.com/boppreh/mouse).

- Testing the speed of this library and benchmarking it against others. For now it will work as a test bed. To my knowledge, the speed is reliable. 
