# Star Wars

Star Wars is a game implemented in **PYTHON** library **Pygame**. To steer the spaceship we use **Mediapipe**, which is a library that uses **Artificial Intelligence** to recognize and map the positions of the points on your hands.
Our goal is to collect as many points as we can, you collect them by catching gems. You also have to look for asteroids and enemy spaceships, you can simply run from them or shoot them with a laser. If they hit you you will lose life points, you can restore them by catching tools. With more points, objects are appearing with higher velocity. 
To steer the spaceship you need to pretend that you are holding a wheel, like you would do while driving a car. 
The stronger you turn, the faster the spaceship will turn. You shoot laser by giving the thumbs up with both of your hands, while the rest of the fingers are folded.
## Tips for better steering:
1. Make sure your palms are visible for the camera.
2. Make sure you have a good lighting and the camera sees you clearly.
3. Try to avoid rapid movements of hands, so they wouldn't look blurry for the camera.
4. Try to remember to keep your hands in fist positions (fingers folded).

If you'll be a good enough pilot you can cover yourself with glory and earn places in the ranks of 5 the best pilots in the galaxy!!!
 
 ## Demo of a game
![sg](https://user-images.githubusercontent.com/73268650/118136149-13ccf480-b404-11eb-81db-224dae58101e.gif)


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
pip install opencv-python==4.5.1.48 numpy==1.19.2 pygame==2.0.1 mediapipe==0.8.3.1 msvc-runtime
```
Installing using pip

``` bash
pip install opencv-python==4.5.1.48 numpy==1.19.2 pygame==2.0.1 mediapipe==0.8.3.1 msvc-runtime
```
If pip can't find right version of libraries upgrade pip and pip install again

``` bash
pip install --upgrade pip
```
To play type into command window(make sure you are in the right repository):
``` bash
python main.py
```
You can change some parameters of the game through command line arguments or simply change them in the code
``` bash
python main.py --width 1000 --height 1000 --camera 0 --initial_speed 10 --speed_jump 2 --folder_levels star_wars
```
You can add folder with images to 'assets/levels/'.
Just make sure you order them correctly (1.png, 2.jpg, 3.png, ...)
![image](https://user-images.githubusercontent.com/73268650/118181763-7213ca80-b438-11eb-9aa5-5a0a2206dffa.png)


