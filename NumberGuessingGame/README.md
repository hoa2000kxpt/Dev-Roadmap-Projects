# 🎮 Number Guessing Game

A fun, interactive CLI-based number guessing game built with Python. Test your luck and intuition as you try to guess a randomly selected number between 1 and 100 within a limited number of chances.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Difficulty Levels](#difficulty-levels)
- [Game Features](#game-features)
- [Testing](#testing)
- [File Structure](#file-structure)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Features
- 🎯 Randomly generated number between 1 and 100
- 🎮 Three difficulty levels with varying chances
- 💡 Smart hint system to assist players
- 🏆 High score tracking across multiple rounds
- ⏱️ Built-in timer to track game duration
- 🔄 Play multiple rounds without restarting

### Advanced Features
- Difficulty-based hint allocation
- Persistent high score tracking per difficulty level
- Input validation with helpful error messages
- User-friendly CLI interface with visual feedback
- Ability to play multiple rounds continuously

## 🔧 Requirements

- Python 3.7 or higher
- pytest (for running tests)
- pytest-mock (for running tests)

## 📦 Installation

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd number-guessing-game

# Or download the files directly
```

### Step 2: Install Dependencies
```bash
# Install pytest and pytest-mock for testing
pip install pytest pytest-mock
```

### Step 3: Verify Installation
```bash
# Check Python version
python --version

# Check pytest installation
pytest --version
```

## 🚀 Usage

### Running the Game
```bash
python number_guessing_game.py
```

### Running Tests
```bash
# Run all tests
pytest number_guessing_game_tests.py -v

# Run specific test class
pytest number_guessing_game_tests.py::TestInputValidation -v

# Run with coverage report
pytest number_guessing_game_tests.py --cov=number_guessing_game --cov-report=html
```

## 🎮 Game Rules

1. The computer randomly selects a number between 1 and 100
2. You have a limited number of chances based on the selected difficulty level
3. For each guess, you receive feedback:
   - "The number is greater than X" if your guess is too low
   - "The number is less than X" if your guess is too high
   - "Congratulations!" if you guess correctly
4. Guess the number correctly to win and progress to the next round
5. Run out of chances to lose the current round
6. You can use hints strategically to help narrow down the number

## 📊 Difficulty Levels

| Difficulty | Chances | Hints | Best For |
|------------|---------|-------|----------|
| **Easy** | 10 | 3 | Beginners, Casual Players |
| **Medium** | 5 | 2 | Intermediate Players |
| **Hard** | 3 | 1 | Experienced Players, Challenge Seekers |

## 🎯 Game Features

### Hint System
- Type `h` at any time to use a hint
- Hints reveal whether the secret number is even or odd
- Limited hints per difficulty level
- Once hints are exhausted, you can't request more

### High Score Tracking
- Tracks the minimum number of attempts for each difficulty
- Persists across multiple rounds
- Displayed after each game
- Shows new high scores with a trophy emoji

### Timer
- Automatically tracks time from game start to completion
- Displayed in the results screen
- Shows how quickly you can guess the number

### Input Validation
- Validates that guesses are numbers between 1-100
- Provides helpful error messages for invalid input
- Allows easy retry on invalid input

## 🧪 Testing

The project includes a comprehensive test suite with 60+ test cases covering:

- **Game Initialization**: Setup and configuration
- **Difficulty Selection**: All difficulty levels and error handling
- **Hint System**: Hint consumption and hint logic
- **Game Logic**: Core guessing mechanics
- **Input Validation**: Boundary conditions and edge cases
- **High Score Tracking**: Score persistence and updates
- **Win/Loss Conditions**: Victory and defeat scenarios
- **Integration Tests**: Complete game flow

### Running Tests

```bash
# Run all tests with verbose output
pytest number_guessing_game_tests.py -v

# Run tests with short traceback
pytest number_guessing_game_tests.py -v --tb=short

# Run specific test class
pytest number_guessing_game_tests.py::TestInputValidation -v

# Generate coverage report (HTML)
pytest number_guessing_game_tests.py --cov=number_guessing_game --cov-report=html

# Generate coverage report (terminal)
pytest number_guessing_game_tests.py --cov=number_guessing_game
```

### Test Coverage

The test suite provides comprehensive coverage across:
- ✅ Unit tests for individual components
- ✅ Integration tests for game flow
- ✅ Edge case and boundary testing
- ✅ Input validation testing
- ✅ Game state management

## 📁 File Structure

```
number-guessing-game/
├── number_guessing_game.py      # Main game logic and implementation
├── number_guessing_game_tests.py # Comprehensive test suite
├── README.md                     # This file
└── .gitignore                   # Git ignore file (optional)
```

## 💻 Examples

### Example Game Session

```
============================================================
🎮 Welcome to the Number Guessing Game! 🎮
============================================================

RULES:
1. I'm thinking of a number between 1 and 100.
2. You have a limited number of chances based on difficulty.
3. After each guess, I'll tell you if the number is higher or lower.
4. Guess correctly to win! Run out of chances to lose.
5. You can use hints to help you (limited per difficulty level).
============================================================

Please select the difficulty level:
1. Easy (10 chances, 3 hints)
2. Medium (5 chances, 2 hints)
3. Hard (3 chances, 1 hint)
Enter your choice (1/2/3): 2

✨ Great! You have selected the Medium difficulty level.
   Chances: 5 | Hints: 2
   Let's start the game!

Enter your guess (1-100) or 'h' for hint: 50
📉 Incorrect! The number is less than 50.
   Remaining chances: 4

Enter your guess (1-100) or 'h' for hint: 25
📈 Incorrect! The number is greater than 25.
   Remaining chances: 3

Enter your guess (1-100) or 'h' for hint: h
💡 Hint: The number is odd. (1 hints left)

Enter your guess (1-100) or 'h' for hint: 35
📉 Incorrect! The number is less than 35.
   Remaining chances: 2

Enter your guess (1-100) or 'h' for hint: 29
🎉 Congratulations! You guessed the correct number!
   Number: 29
   Attempts: 4
   Time: 45.2 seconds
   High Score for medium: 4
============================================================

Do you want to play again? (yes/no): no

============================================================
Thanks for playing! See you next time! 👋
============================================================
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Ensure all tests pass before submitting a PR
- Add new tests for new features
- Follow PEP 8 style guidelines
- Update README.md if adding new features

## 📝 Future Enhancements

Possible features for future versions:

- [ ] Difficulty presets with custom ranges
- [ ] Leaderboard with player rankings
- [ ] Different game modes (reverse guessing, etc.)
- [ ] Sound effects and visual animations
- [ ] Multiplayer mode
- [ ] Persistent storage of high scores to file
- [ ] Statistics dashboard
- [ ] Difficulty progression system

## 🐛 Known Issues

- None currently reported

If you find any bugs, please report them by opening an issue in the repository.

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 👨‍💻 Author

Created as a Python learning project for implementing game logic, testing practices, and CLI applications.

## 🙏 Acknowledgments

- Python community for excellent documentation
- Pytest team for the testing framework
- All contributors and testers

## 📞 Support

For support, questions, or suggestions:
- Open an issue on the repository
- Check existing issues for similar questions
- Review the test cases for usage examples

---

**Have fun playing! 🎮** Can you guess the number before running out of chances?
