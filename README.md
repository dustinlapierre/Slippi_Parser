# Randall the AI Melee commentator

This was an experiment/proof of concept of mine for an AI commentator. 
Randall leveraged a Long Short-Term Memory Recurrent Neural Network
to recognized high level techniques utilized by professional
Super Smash Bros. Melee players. This task required manual creation
of training sets and a custom memory parser that read from game
memory while it was played, allowing Randall
to "watch" the game. Randall is currently only able to recognize 
"Dash Dancing," wherein one player runs in the direction of the 
opponent, inching closer, before darting away again. The methods 
used herein could be extended to cover more play patterns, until 
Randall became a competent play-by-play commentator. In the mean 
time though, I have added a statistical analysis module that allows 
Randall to study the data readily available in the memory to produce 
filler commentary. This project was mostly abandoned in 2018.

##Screenshots
![Example 1](https://github.com/dustinlapierre/Slippi_Parser/blob/master/images/Screen_AI1.png?raw=true)
![Example 2](https://github.com/dustinlapierre/Slippi_Parser/blob/master/images/Screen_AI2.png?raw=true)
![Example 3](https://github.com/dustinlapierre/Slippi_Parser/blob/master/images/Screen_AI3.png?raw=true)
![Game Emulation](https://github.com/dustinlapierre/Slippi_Parser/blob/master/images/game_screen.png?raw=true)

##Setup instructions
I do not recommend trying to get this running, as it is quite a hassle.
For Windows:
1. Install Python
2. Install Tensorflow
3. Install CUDA
4. Install cuDNN
5. Install Kivy
6. Place the entire Slippi_Parser folder into the Slippi folder of
the Slippi edition of the Dolphin emulator. 
(This was made with a beta version of the emulator and hasn't been
tested on modern versions)
7. Run "python memory_parser.py" from the project folder, which should
hang shortly after the Kivy initializes up to the Images.
8. Open Dolphin and run SSBM
9. Start a match, and Randall will automatically recognize when
the game has started and open the commentary window.