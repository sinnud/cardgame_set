# SET Card Game

A Python implementation of the classic SET card game with a graphical user interface.

## About SET

SET is a real-time card game where players identify patterns in cards with different shapes, colors, numbers, and shadings. A valid SET consists of three cards where each property is either all the same or all different across the three cards.

## Features

- Interactive GUI using Python's tkinter
- Visual card representations with shapes, colors, and patterns
- Score tracking and game statistics
- Help system with complete rules
- "Give Up" option to add more cards when stuck

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

### Platform-Specific Setup

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (RHEL/CentOS/Fedora):**
```bash
sudo yum install tkinter
# or
sudo dnf install python3-tkinter
```

**Linux (Arch):**
```bash
sudo pacman -S tk
```

**Windows:**
Tkinter is typically included with Python installations.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sinnud/cardgame_set.git
cd cardgame_set
```

2. Create and activate virtual environment:

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

## Running the Game

```bash
python src/set_gui.py
```

## How to Play

1. **Objective:** Find valid SETs among the displayed cards
2. **Selection:** Click up to 3 cards to select them
3. **Validation:** After selecting 3 cards, the game checks if they form a valid SET
4. **Scoring:** +1 for correct SET, -1 for incorrect guess
5. **Give Up:** Add 3 more cards when stuck (limited to 3 times)

## SET Rules

A valid SET consists of three cards where **each property** is either:
- **ALL THE SAME** across the 3 cards, OR  
- **ALL DIFFERENT** across the 3 cards

### Properties:
- **Shape:** Circle (○), Triangle (△), Square (□)
- **Color:** Red, Green, Blue  
- **Number:** 1, 2, or 3 shapes
- **Shading:** Outline, Striped, Filled

### Examples:
✅ **VALID SET:** All same color, all different shapes, all same number  
✅ **VALID SET:** All different colors, all same shape, all different numbers  
❌ **INVALID:** 2 red cards + 1 blue card (not all same, not all different)

## Project Structure

```
cardgame_set/
├── src/
│   ├── core.py      # Game logic and SET validation
│   └── set_gui.py   # GUI interface using tkinter
├── requirements.txt # Dependencies (none required)
└── README.md       # This file
```

## License

This project is open source.