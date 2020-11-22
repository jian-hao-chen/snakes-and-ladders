# Reinforcement Learning - Assignment 1
A `Snakes and Ladders` game for Reinforcement Learning algorithms.

## Install
1. Create a virtual python environment in the directory, and enter it. (**Optional**)
```bash
$ virtualenv venv
```
Enter the virtual environment after the environment is created successfully.
```bash
# Windows
$ venv\Scripts\activate.bat
# Linux / MacOS
$ source venv/bin/activate
```
> If you don't have virtualenv, you can install it by executing `pip install virtualenv`.

2. Install the required packages.
```bash
(venv) $ pip install -r requirements.txt 
```

## How to run
### Usage
```bash
main.py [-h] -v {v0,v1,v2} -s {small,medium,large} [-i INTERVAL]
        [-E EPISODE] [-r RANDOM] [-V] [-a ALPHA] [-y GAMMA]     
        [-e EPSILON] [-l LAMBDA] [-q]
```
### Arguments description
```
optional arguments:
  -h, --help            show this help message and exit

  -v {v0,v1,v2}, --version {v0,v1,v2}
                        select the version of game.

  -s {small,medium,large}, --size {small,medium,large}
                        select the size of game board.

  -i INTERVAL, --interval INTERVAL
                        the interval time of each round. (default: 0.5 sec)

  -E EPISODE, --episode EPISODE
                        how many times to run.

  -r RANDOM, --random RANDOM
                        how many random dice. (default: 0)

  -V, --visualize       set to display the training process.

  -a ALPHA, --alpha ALPHA
                        learning rate. (default: 0.1)

  -y GAMMA, --gamma GAMMA
                        decay rate. (default: 0.9)

  -e EPSILON, --epsilon EPSILON
                        epsilon used in `eps-greedy`. (default: 0.2)

  -l LAMBDA, --lambda LAMBDA
                        lambda used in `TD(lambda)`. (default: 0.9)

  -q, --q               Use Q-Learning as training policy.
```

For example:
```
$ python main.py -v v0 -s small -E 10 -V
```
This command will run a **v0** version evaluation with **100 spots** for **10 episodes** and save the results as an `.png` image.