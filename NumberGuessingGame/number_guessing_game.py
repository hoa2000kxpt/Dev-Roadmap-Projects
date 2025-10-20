import random
import time

class NumberGuessingGame:
    def __init__(self):
        self.high_scores = {'easy': float('inf'), 'medium': float('inf'), 'hard': float('inf')}
        self.difficulty_map = {
            '1': {'name': 'Easy', 'chances': 10, 'hints': 3},
            '2': {'name': 'Medium', 'chances': 5, 'hints': 2},
            '3': {'name': 'Hard', 'chances': 3, 'hints': 1}
        }

    def display_welcome(self):
        print("\n" + "="*60)
        print("🎮 Welcome to the Number Guessing Game! 🎮".center(60))
        print("="*60)
        print("\nRULES:")
        print("1. I'm thinking of a number between 1 and 100.")
        print("2. You have a limited number of chances based on difficulty.")
        print("3. After each guess, I'll tell you if the number is higher or lower.")
        print("4. Guess correctly to win! Run out of chances to lose.")
        print("5. You can use hints to help you (limited per difficulty level).")
        print("="*60 + "\n")

    def select_difficulty(self):
        while True:
            print("Please select the difficulty level:")
            print("1. Easy (10 chances, 3 hints)")
            print("2. Medium (5 chances, 2 hints)")
            print("3. Hard (3 chances, 1 hint)")
            choice = input("Enter your choice (1/2/3): ").strip()
            
            if choice in self.difficulty_map:
                difficulty = self.difficulty_map[choice]['name'].lower()
                config = self.difficulty_map[choice]
                print(f"\n✨ Great! You have selected the {config['name']} difficulty level.")
                print(f"   Chances: {config['chances']} | Hints: {config['hints']}")
                print("   Let's start the game!\n")
                return difficulty, config
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.\n")

    def use_hint(self, secret_number, low, high, hints_left):
        if hints_left <= 0:
            print("❌ No hints left!")
            return hints_left
        
        hints_left -= 1
        if secret_number % 2 == 0:
            print(f"💡 Hint: The number is even. ({hints_left} hints left)")
        else:
            print(f"💡 Hint: The number is odd. ({hints_left} hints left)")
        
        return hints_left

    def play_round(self):
        self.display_welcome()
        difficulty, config = self.select_difficulty()
        
        secret_number = random.randint(1, 100)
        chances = config['chances']
        hints_left = config['hints']
        attempts = 0
        start_time = time.time()

        while chances > 0:
            try:
                guess_input = input(f"Enter your guess (1-100) or 'h' for hint: ").strip()
                
                if guess_input.lower() == 'h':
                    hints_left = self.use_hint(secret_number, 1, 100, hints_left)
                    continue
                
                guess = int(guess_input)
                
                if guess < 1 or guess > 100:
                    print("⚠️  Please enter a number between 1 and 100.\n")
                    continue
                
                attempts += 1
                
                if guess == secret_number:
                    elapsed_time = time.time() - start_time
                    print("\n" + "="*60)
                    print(f"🎉 Congratulations! You guessed the correct number!")
                    print(f"   Number: {secret_number}")
                    print(f"   Attempts: {attempts}")
                    print(f"   Time: {elapsed_time:.1f} seconds")
                    
                    if attempts < self.high_scores[difficulty]:
                        self.high_scores[difficulty] = attempts
                        print(f"   🏆 New High Score for {difficulty.capitalize()}!")
                    else:
                        print(f"   High Score for {difficulty.capitalize()}: {self.high_scores[difficulty]}")
                    print("="*60 + "\n")
                    return
                
                elif guess < secret_number:
                    print(f"📈 Incorrect! The number is greater than {guess}.")
                else:
                    print(f"📉 Incorrect! The number is less than {guess}.")
                
                chances -= 1
                print(f"   Remaining chances: {chances}\n")
            
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.\n")
                continue

        print("\n" + "="*60)
        print(f"❌ Game Over! You've run out of chances.")
        print(f"   The correct number was: {secret_number}")
        print(f"   You made {attempts} attempts.")
        print("="*60 + "\n")

    def display_high_scores(self):
        print("\n🏆 HIGH SCORES 🏆")
        print("-" * 40)
        for difficulty in ['easy', 'medium', 'hard']:
            score = self.high_scores[difficulty]
            display_score = str(score) if score != float('inf') else "No score yet"
            print(f"{difficulty.capitalize():10} | {display_score}")
        print("-" * 40 + "\n")

    def run(self):
        while True:
            self.play_round()
            self.display_high_scores()
            
            play_again = input("Do you want to play again? (yes/no): ").strip().lower()
            if play_again not in ['yes', 'y']:
                print("\n" + "="*60)
                print("Thanks for playing! See you next time! 👋".center(60))
                print("="*60 + "\n")
                break

if __name__ == "__main__":
    game = NumberGuessingGame()
    game.run()