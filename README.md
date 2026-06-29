*This project has been created as part of the 42 curriculum by frasomal, nocurely.*

# Description

`Pac-man` is an arcade game where you guide a character, Pac-man, through a series of maze while attempting to escape ghosts. The goal is to collect pacgums and super-pacgums to increase the score.

If the player touches any ghost, they lose a life. Once they lose all lives, they lose the game. The player only lives if they complete all levels.

# Instructions

To run mandatory evaluations:

```sh
make install
make lint # make lint-strict
make run ./config.json # make debug ./config.json
```

Once inside the program, you may toggle on and off by navigating to the cheat button and pressing the enter key.

```txt
# current cheats

invincibility:  'I'
noclip:         'N'
freeze ghosts:  'F'
skip level:     'G'
extra life:     'L'
reduce speed:   'O'
increase speed: 'P'

# character movement

up:             'arrow_up'
down:           'arrow_down'
left:           'arrow_left'
right:          'arrow_right'

# your character collects pacgums and super-pacgums when hovering over them automatically
```

Whether you use cheat mode or not does not affect the final score.
Your score is automatically written to ./src/saves/highscores.json when finalizing your name.

Use the following command to clean up the project: `make clean`

# Resources

Here are some references we've used for the making of the project:
- [pygame](https://www.pygame.org): Documentation for pygame.
- [sprites](https://i.pinimg.com/736x/7d/38/cf/7d38cf13f2f91bbdf067b8b8522b44f7.jpg): Sprites used for the project.
- The colour scheme was directly inspired from the subject's representation of the game.
- [colour scheme](https://coolors.co/3c5ac8-ff0000-f2c5ff-ffb751-00ffff-ffff00-19191e-ffb897-ffe6b4): Colours used for the project.
- AI has been used to solve some annoying parts of the project, such as the AI for the ghosts and a bug where Pac-man would get stuck between two gaps.

# Configuration

```txt
# config.json

- highscore_filename: the file to use to store highscores
- lives: the number of lives the player starts with
- pacgum: the number of pacgums in the game. super-pacgums are a fixed value of 4
- points_per_pacgum: the number of points a pacgum is worth, default: 10
- points_per_super_pacgum: the number of points a super-pacgum is worth: default: 50
- points_per_ghost: the number of points a ghost is worth, default: 200
- seed: the first level's seed, default: 42
- level_max_time: the overall duration of a level, default: 90
```

# Highscore

The highscore system is simple. When finishing the game and inputting your name (after a gameover), your score is submitted to a .json file located in ./src/saves. It is sorted by score, from best to worst.

It is possible to view the highscores from the menu but also from the .json itself so you can reuse it in another project if wanted.

Writing to a .json file was simply the cleanest way to fetch and display scores.

# Maze Generation

The mazes are generated using the package provided by the project itself. You can find it in the root directory: `./mazegenerator/`

The package is also provided as a wheel file: `./mazegenerator-2.0.2-py3-none-any.whl`

It is left untouched. You may use the following commands to extract and compare:

```txt
unzip ./mazegenerator-2.0.2-py3-none-any.whl -d mazegenerator-2
diff -rq ./mazegenerator ./mazegenerator-2
```

A maze is generated when the player first enters `START GAME`, then it is generated for each level after this one. It's a simple call that is then translated into a pygame surface and blitted onto the screen.

# Implementation

See the `Maze Generation` section for implementations regarding maze generation.

To implement the AI for the ghosts, it was an algorithm that was given to a single component * 4.

For Pac-man, it is self-explanatory.

All sprites are implemented via ./src/game/spritesheet/

In general, we keep using ./src/scenes/game.py and ./src/scenes/scene.py to link scripts with each other.

A lot of modules and classes are components, which means they can be used in other projects.

```txt
$> eza --tree --icons --only-dirs
 . # root dir
├──  assets
├──  fonts
├──  mazegenerator
├──  mazegenerator-2.0.2.dist-info
├──  sound
└──  src
    ├──  __pycache__
    ├──  game
    │   └──  spritesheet
    ├──  saves
    ├──  scenes
    │   └──  __pycache__
    └──  ui
```

# General Software Architecture

See the `Implementation` section for details about modules and classes.

# Project Management

To finalize the project, we used a mutual git repository and Discord to communicate, though the work has been done at school most of the time. We were able to work on separate parts of the project at the same time which caused no merge issues and agreed on which file each person should work on.
