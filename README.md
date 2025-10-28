# Advanced Tetris Game

A complete implementation of the classic Tetris game using Python and Pygame.

## Features

- All 7 standard Tetris pieces (I, O, T, S, Z, J, L) with distinct colors
- Next piece preview
- Scoring system with level progression
- Line clearing mechanics
- Increasing difficulty as levels progress
- Pause/resume functionality
- Game over detection with restart option
- Keyboard controls with key repeat
- Sound effects support

## Installation

1. Make sure you have Python 3 installed on your system
2. Install Pygame using pip:
   ```
   pip install pygame
   ```

## How to Play

1. Clone or download this repository
2. Navigate to the directory containing `tetris_game.py`
3. Run the game:
   ```
   python tetris_game.py
   ```

## Controls

- Arrow Left/Right: Move piece horizontally
- Arrow Down: Soft drop (move down faster)
- Arrow Up: Rotate piece
- Space: Hard drop (instantly drop to bottom)
- P: Pause/Resume game
- R: Restart game

## Game Mechanics

- Score points by clearing lines (1 line = 100, 2 lines = 300, 3 lines = 500, 4 lines = 800)
- Every 10 lines cleared increases the level by 1
- Higher levels increase the falling speed of pieces
- Game ends when a new piece cannot be placed at the top of the grid

## Code Structure

- `Tetromino` class: Represents a single falling piece with shape, color, and rotation
- `Game` class: Handles all game logic, controls, rendering, scoring, and state management
- Constants at the top of the file define game parameters and colors

## Files

- `tetris_game.py` - Main game implementation
- `README.md` - This file
