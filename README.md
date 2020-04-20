Using this project to learn reinforcement learning. 

# Current TO-DO list

### 1. Launch game and gather screenshots on headless servers.
---
In order to use distributed training, I'd like to be able to use headless cloud instances to run the game and pull the data. Currently, I am able to gather screenshots of the game at around 60 FPS which is FAR more than I need. I need to find an effective way to run the game (in an X display?).

I'm not well versed on this topic but I am doing a lot of research.

Also, the best method may be creating an OpenAI gym. That will just be an improvment and a dream really.

### 2. Give bot actions that it can use.
---
                Actions


      Nothing

      Adjust View:
        X: [-10, 10] in degrees
        Y: [-10, 10] in degrees
        Delay: [int]

      Move:
        Direction: [W, S, A, D]

      Move Depth:
        [Jump, Crouch, Walk]

      Change Weapon:
        [1, 2, 3, 4, 5, 6, 7, 8, 9]

      Attack:
        [Left Click, Right Click]

      Reload:
        [1 or 0]

      Interact (doors, plant, etc):
      [1 or 0]

      Buy:
        [Buy Binds]


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

### 3. Create an OpenAI gym for CSGO
---
This may prove to be difficult but would make writing this bot much easier. Also, it could help with training distribution.
