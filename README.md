Using this project to learn reinforcement learning. Below are the actions that the bot should be able to make.


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
