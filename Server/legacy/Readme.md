# Notes for gamestate (observation) capture

### Gather CSGO client data:

Once CSGO is running, we launch a server to capture specific data about the client. This is used for observation and the reward function.


                State Variables

      Round Phase: [Playing, Buy]
      Team Alive: [1-5]
      Enemy Alive: [1-5]
      Bomb Planted: [1 or 0]
      Ammo in Mag: [int]
      Total Ammo: [int]
      Rounds Won: [int]
      Rounds Lost: [int]
      Personal Score: [int]
      Health: [int]
      Armor: [int]
