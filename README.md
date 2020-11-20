Using this project to learn reinforcement learning. 

# How it works *So far*

### 1. Launch game and gather screenshots on headless servers.
---

*See ```ScreenCapture``` folder*


Game is launched inside of a Xvfb virtual display with VirtualGL enabled.

### 2. Gather observations on running game.
---

Observations consist of two things:

1. Screenshot of current state
2. Gamestate observation (*See ```Server``` folder*)

These observations are what get transfered to the model in order to decide on the next step and calculate reward.

### 3. Give bot actions that it can use.
---

Based on the observation, the model decides on what the action should be for the next step. Listed, is a readable for of what the agent can do:

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


### 4. Apply reward
---

I think there should be some exploration reward, especially at the beginning of training. Some reward just for moving and visiting new places would be a good idea. Obviously rewarding frags, bomb plants, round wins, match wins, etc. are very important but I will be looking more into that with time.


---
---
# Looking Forward

I really would like CSGO to be merely a building block into what I believe could change machine learning. My goal is to first implement CSGO to gain a bit of traction and then move to include any Steam game. This way, different machine learning techniques can be tested against a vast number of environments very easily.

Also, it might be possible to create clients for players to use to record their own gameplay in order to jumpstart learning.

Lastly, distributed training using containerization could boost performance infinitly. [See more](https://arxiv.org/abs/1803.00933)
