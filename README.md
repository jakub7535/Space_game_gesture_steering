# Star Wars

Star Wars is game implemented in **PYTHON** using **Pygame** library that uses **Artificial Inteligence** to recognize and map the positions of points on your hands.
Our goal is to collect as many points as we can, you collect them by catching gems. You also have to look for asteroids, you can simply run from them or shoot them with laser. With more points, objects are apearing with higher velocity. 
To steer the spaceship you need to pretend that you are holding a wheel, like you do while driving a car. 
The stronger you turn the faster the spaceship will turn. You shoot laser by giving the thumbs up with both of your hands, while the rest of the fingers are folded.
## Tips for better steering:
1. Make sure your palms are visable for camera.
2. Make sure you have a good lighting and camera sees you clearly.
3. Try to avoid rapid movements of hands, so they wouldn't look blurry for the camera.
4. Try to remember to keep your hands in fist positions (fingers folded).
If you'll be good enough pilot you can cover yourself with glory and earn places in ranks of 5 the best pilots in the galaxy!!!
 
 ## Demo of a game
 <p align="center"><img src="assets/assets_readme/demo2.gif"\></p>

## How to run 
To run this program:
1. Clone repository from github and enter the project.
2. Install required liberaries via Pip or Anaconda(rocomended).
3. Run main.py and enjoy game.

# Instalation
First clone this repository using git 

``` bash
git clone https://github.com/jakub7535/Space_game_gesture_steering.git
```
or simply  download and unpack the ZIP file(change folder name if needed from 'Space_game_gesture_steering-master' to 'Space_game_gesture_steering' for convenience.

![image](https://user-images.githubusercontent.com/73268650/118058544-b8145400-b38e-11eb-9a13-d282dfaf65e8.png)

Then enter the repository:

![image](https://user-images.githubusercontent.com/73268650/118058724-248f5300-b38f-11eb-91aa-c8569f5037d3.png)

Installing using conda(recomended) and virtual environment

``` bash
conda create --name Space_game python=3.8.5
conda activate Space_game
pip install opencv-python==4.5.1.48 numpy==1.19.2 pygame==2.0.1 mediapipe==0.8.3.1
```
Installing using pip

``` bash
pip install opencv-python==4.5.1.48 numpy==1.19.2 pygame==2.0.1 mediapipe==0.8.3.1
```
