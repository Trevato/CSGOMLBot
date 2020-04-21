# Client Gather notes

### This is where everything comes together:

I think the best method for training is to create a [Tensorflow Environment](https://www.tensorflow.org/agents/tutorials/2_environments_tutorial).

---

### How to set it up:

We need a few things:

  1. Observation - *This will be the screen capture.*  
    
  2. State - *This will be what is returned from the Gamestate server*
  
  3. Reward - *This will be a calculation based on the state*
  
Given these things, we can create an environment where TF Agents can learn easily.

---

### Why use TF Environments?

1. Easily test different Agents
2. Easily expandable to other games
3. [Parallelization](https://arxiv.org/abs/1709.02878)
