
# Fruit Ninja - Pygame

A Fruit Ninja-style game developed using Python and Pygame. The player slices fruits using mouse movement, avoids bombs, and tries to achieve the highest possible score.

## Features

- Fruit slicing using mouse movement
- Improved collision detection for fast mouse swipes
- Score tracking
- Bomb collision detection
- Life system for missed fruits
- Game Over screen displaying the final score
- Easy, Medium, and Hard difficulty levels
- Restart and exit options
- Sound effects for fruit slicing, bomb collisions, and Game Over

## Technologies Used

- Python
- Pygame

## Requirements

- Python 3.10 or later
- Pygame

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SruthiVejju/LAB4_FruitNinja_SruthiVejju_PES1UG24CS472-.git
```

### 2. Navigate to the Project Folder

```bash
cd 41_fruit-ninja
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Game

Run the following command from the project directory:

```bash
python main.py
```

## How to Play

1. Move the mouse across the screen to slice fruits.
2. Slice fruits to increase your score.
3. Avoid slicing bombs.
4. Avoid missing too many fruits, as missed fruits reduce your lives.
5. When the game ends, the Game Over screen displays your final score.
6. Select a difficulty level to restart the game, or select Exit to close it.
7. Press `Esc` to exit the game.

## Difficulty Levels

| Level | Fruit Spawn Rate | Bomb Probability |
|-------|------------------|------------------|
| Easy | Slow | Low |
| Medium | Moderate | Moderate |
| Hard | Fast | High |

## Improvements Implemented

### 1. Improved Collision Detection

Implemented line-segment collision detection to improve the detection of fast mouse swipes and reduce missed fruit slices.

### 2. Game Over Screen

Added a Game Over screen that displays the final score when a bomb is sliced or all lives are lost.

### 3. Difficulty Selection

Added Easy, Medium, and Hard difficulty levels with different fruit spawn rates and bomb probabilities.

### 4. Replay Functionality

Added options to restart the game with a selected difficulty or exit the game.

### 5. Sound Effects

Added sound effects for fruit slicing, bomb collisions, and the Game Over event.

## Project Structure

```text
41_fruit-ninja/
├── main.py
├── requirements.txt
├── README.md
└── game/
    ├── __init__.py
    ├── game_engine.py
    └── fruit.py
```

## Testing

The following functionalities were checked:

- Fruit slicing and score updates
- Collision detection during mouse movement
- Bomb collision and Game Over behavior
- Final score display
- Difficulty selection
- Restart and exit options
- Sound effects

## Lab Submission

This project was updated as part of the VibeCoding Lab assignment.

The submission includes:

- Updated source code
- Original gameplay video (10 seconds)
- Improved gameplay video (10 seconds)
- Exported ChatGPT conversation history

## Submitted by:

Sruthi Vejju
PES1UG24CS472
PES University
