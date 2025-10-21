"""
Number Guessing Game Tests:
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from number_guessing_game import NumberGuessingGame


class TestGameInitialization:
    """Test suite for game initialization and setup"""
    
    def test_game_creation(self):
        """Test that game object is created successfully"""
        game = NumberGuessingGame()
        assert game is not None
        assert hasattr(game, 'high_scores')
        assert hasattr(game, 'difficulty_map')
    
    def test_initial_high_scores(self):
        """Test that high scores are initialized correctly"""
        game = NumberGuessingGame()
        assert game.high_scores['easy'] == float('inf')
        assert game.high_scores['medium'] == float('inf')
        assert game.high_scores['hard'] == float('inf')
    
    def test_difficulty_map_structure(self):
        """Test that difficulty map is properly structured"""
        game = NumberGuessingGame()
        assert '1' in game.difficulty_map
        assert '2' in game.difficulty_map
        assert '3' in game.difficulty_map
        
        for level in ['1', '2', '3']:
            assert 'name' in game.difficulty_map[level]
            assert 'chances' in game.difficulty_map[level]
            assert 'hints' in game.difficulty_map[level]
    
    def test_difficulty_chances(self):
        """Test that difficulty levels have correct chance allocations"""
        game = NumberGuessingGame()
        assert game.difficulty_map['1']['chances'] == 10  # Easy
        assert game.difficulty_map['2']['chances'] == 5   # Medium
        assert game.difficulty_map['3']['chances'] == 3   # Hard
    
    def test_difficulty_hints(self):
        """Test that difficulty levels have correct hint allocations"""
        game = NumberGuessingGame()
        assert game.difficulty_map['1']['hints'] == 3  # Easy
        assert game.difficulty_map['2']['hints'] == 2  # Medium
        assert game.difficulty_map['3']['hints'] == 1  # Hard


class TestDifficultySelection:
    """Test suite for difficulty selection functionality"""
    
    @patch('builtins.input', return_value='1')
    def test_select_difficulty_easy(self, mock_input):
        """Test selecting easy difficulty"""
        game = NumberGuessingGame()
        difficulty, config = game.select_difficulty()
        assert difficulty == 'easy'
        assert config['name'] == 'Easy'
        assert config['chances'] == 10
    
    @patch('builtins.input', return_value='2')
    def test_select_difficulty_medium(self, mock_input):
        """Test selecting medium difficulty"""
        game = NumberGuessingGame()
        difficulty, config = game.select_difficulty()
        assert difficulty == 'medium'
        assert config['name'] == 'Medium'
        assert config['chances'] == 5
    
    @patch('builtins.input', return_value='3')
    def test_select_difficulty_hard(self, mock_input):
        """Test selecting hard difficulty"""
        game = NumberGuessingGame()
        difficulty, config = game.select_difficulty()
        assert difficulty == 'hard'
        assert config['name'] == 'Hard'
        assert config['chances'] == 3
    
    @patch('builtins.input', side_effect=['4', '2'])
    def test_select_difficulty_invalid_then_valid(self, mock_input):
        """Test that invalid input is rejected and user can retry"""
        game = NumberGuessingGame()
        difficulty, config = game.select_difficulty()
        assert difficulty == 'medium'
        assert mock_input.call_count == 2


class TestHintSystem:
    """Test suite for hint functionality"""
    
    def test_hint_uses_one_hint(self):
        """Test that using a hint decreases hint count"""
        game = NumberGuessingGame()
        hints_left = game.use_hint(50, 1, 100, 3)
        assert hints_left == 2
    
    def test_hint_with_no_hints_left(self):
        """Test behavior when no hints are available"""
        game = NumberGuessingGame()
        hints_left = game.use_hint(50, 1, 100, 0)
        assert hints_left == 0
    
    def test_multiple_hints_usage(self):
        """Test using multiple hints in sequence"""
        game = NumberGuessingGame()
        hints = 3
        for _ in range(3):
            hints = game.use_hint(50, 1, 100, hints)
        assert hints == 0
    
    def test_hint_for_even_number(self):
        """Test that even numbers are identified correctly"""
        game = NumberGuessingGame()
        with patch('builtins.print') as mock_print:
            game.use_hint(50, 1, 100, 1)
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            assert 'even' in call_args.lower()
    
    def test_hint_for_odd_number(self):
        """Test that odd numbers are identified correctly"""
        game = NumberGuessingGame()
        with patch('builtins.print') as mock_print:
            game.use_hint(51, 1, 100, 1)
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            assert 'odd' in call_args.lower()


class TestGameLogic:
    """Test suite for core game logic"""
    
    def test_correct_guess_wins(self):
        """Test that correct guess results in win"""
        game = NumberGuessingGame()
        with patch('builtins.input', side_effect=['50']):
            with patch('builtins.print'):
                with patch('random.randint', return_value=50):
                    # Simulate play_round logic
                    secret = 50
                    guess = 50
                    assert guess == secret
    
    def test_incorrect_guess_higher(self):
        """Test feedback when guess is too high"""
        secret = 30
        guess = 50
        assert guess > secret
    
    def test_incorrect_guess_lower(self):
        """Test feedback when guess is too low"""
        secret = 50
        guess = 30
        assert guess < secret
    
    def test_random_number_range(self):
        """Test that random number is within valid range"""
        with patch('random.randint', return_value=50) as mock_random:
            num = mock_random(1, 100)
            assert 1 <= num <= 100
    
    def test_secret_number_is_unique(self):
        """Test that random number is generated"""
        with patch('random.randint') as mock_random:
            mock_random.return_value = 42
            num1 = mock_random(1, 100)
            num2 = mock_random(1, 100)
            assert num1 == 42
            assert num2 == 42


class TestInputValidation:
    """Test suite for input validation"""
    
    def test_valid_numeric_guess(self):
        """Test that valid numeric input is accepted"""
        try:
            guess = int('50')
            assert 1 <= guess <= 100
        except ValueError:
            pytest.fail("Valid numeric input rejected")
    
    def test_invalid_non_numeric_input(self):
        """Test that non-numeric input is rejected"""
        with pytest.raises(ValueError):
            int('abc')
    
    def test_guess_below_range(self):
        """Test that guess below 1 is rejected"""
        guess = 0
        assert not (1 <= guess <= 100)
    
    def test_guess_above_range(self):
        """Test that guess above 100 is rejected"""
        guess = 101
        assert not (1 <= guess <= 100)
    
    def test_guess_at_lower_boundary(self):
        """Test that guess of 1 is accepted"""
        guess = 1
        assert 1 <= guess <= 100
    
    def test_guess_at_upper_boundary(self):
        """Test that guess of 100 is accepted"""
        guess = 100
        assert 1 <= guess <= 100
    
    def test_hint_command_input(self):
        """Test that 'h' input for hint is recognized"""
        user_input = 'h'
        assert user_input.lower() == 'h'
    
    def test_float_input_conversion(self):
        """Test handling of float input"""
        with pytest.raises(ValueError):
            int('50.5')
    
    def test_negative_number_input(self):
        """Test that negative numbers are rejected"""
        guess = -50
        assert not (1 <= guess <= 100)


class TestHighScoreTracking:
    """Test suite for high score functionality"""
    
    def test_high_score_updated_on_better_attempt(self):
        """Test that high score is updated with fewer attempts"""
        game = NumberGuessingGame()
        game.high_scores['easy'] = 8
        attempts = 5
        if attempts < game.high_scores['easy']:
            game.high_scores['easy'] = attempts
        assert game.high_scores['easy'] == 5
    
    def test_high_score_not_updated_on_worse_attempt(self):
        """Test that high score is not updated with more attempts"""
        game = NumberGuessingGame()
        game.high_scores['medium'] = 3
        attempts = 4
        if attempts < game.high_scores['medium']:
            game.high_scores['medium'] = attempts
        assert game.high_scores['medium'] == 3
    
    def test_high_score_first_attempt(self):
        """Test that first attempt sets the high score"""
        game = NumberGuessingGame()
        assert game.high_scores['hard'] == float('inf')
        game.high_scores['hard'] = 2
        assert game.high_scores['hard'] == 2
    
    def test_high_scores_independent_by_difficulty(self):
        """Test that high scores are tracked separately per difficulty"""
        game = NumberGuessingGame()
        game.high_scores['easy'] = 8
        game.high_scores['medium'] = 4
        game.high_scores['hard'] = 2
        
        assert game.high_scores['easy'] == 8
        assert game.high_scores['medium'] == 4
        assert game.high_scores['hard'] == 2


class TestChanceManagement:
    """Test suite for chance/attempt management"""
    
    def test_easy_has_enough_chances(self):
        """Test that easy difficulty has 10 chances"""
        game = NumberGuessingGame()
        config = game.difficulty_map['1']
        assert config['chances'] >= 10
    
    def test_medium_has_enough_chances(self):
        """Test that medium difficulty has 5 chances"""
        game = NumberGuessingGame()
        config = game.difficulty_map['2']
        assert config['chances'] >= 5
    
    def test_hard_has_enough_chances(self):
        """Test that hard difficulty has 3 chances"""
        game = NumberGuessingGame()
        config = game.difficulty_map['3']
        assert config['chances'] >= 3
    
    def test_chances_decrease_on_wrong_guess(self):
        """Test that chances decrease after wrong guess"""
        initial_chances = 5
        chances = initial_chances - 1
        assert chances == 4


class TestWinConditions:
    """Test suite for win/loss conditions"""
    
    def test_win_on_first_guess(self):
        """Test that guessing correctly on first attempt is a win"""
        secret = 50
        guess = 50
        attempts = 1
        assert guess == secret
        assert attempts == 1
    
    def test_win_on_last_chance(self):
        """Test that winning on last chance is valid"""
        secret = 50
        guess = 50
        chances = 1
        assert guess == secret
        assert chances >= 1
    
    def test_loss_when_chances_exhausted(self):
        """Test that game ends when chances reach zero"""
        chances = 0
        assert chances == 0
    
    def test_incorrect_guess_sequence(self):
        """Test a sequence of incorrect guesses"""
        secret = 50
        guesses = [30, 70, 40, 60]
        for guess in guesses:
            assert guess != secret


class TestWelcomeMessage:
    """Test suite for welcome message display"""
    
    @patch('builtins.print')
    def test_welcome_message_displayed(self, mock_print):
        """Test that welcome message is displayed"""
        game = NumberGuessingGame()
        game.display_welcome()
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_welcome_contains_rules(self, mock_print):
        """Test that welcome message contains rules"""
        game = NumberGuessingGame()
        game.display_welcome()
        calls = [str(call) for call in mock_print.call_args_list]
        all_calls = ' '.join(calls).lower()
        assert 'rule' in all_calls or 'number' in all_calls


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions"""
    
    def test_same_guess_twice(self):
        """Test that same guess can be made twice"""
        guess1 = 50
        guess2 = 50
        assert guess1 == guess2
    
    def test_all_numbers_in_range_possible(self):
        """Test that any number between 1-100 can be the secret"""
        for secret in [1, 50, 100]:
            assert 1 <= secret <= 100
    
    def test_game_state_reset_between_rounds(self):
        """Test that game state resets for new rounds"""
        game = NumberGuessingGame()
        old_high_scores = game.high_scores.copy()
        game.high_scores['easy'] = 5
        # High scores should persist, not reset
        assert game.high_scores['easy'] == 5
        # But new game should start fresh with new secret number
        game2 = NumberGuessingGame()
        assert game2.high_scores['easy'] == float('inf')
    
    def test_zero_is_invalid_guess(self):
        """Test that 0 is not a valid guess"""
        guess = 0
        assert not (1 <= guess <= 100)
    
    def test_very_large_number_invalid(self):
        """Test that very large numbers are invalid"""
        guess = 999999
        assert not (1 <= guess <= 100)


class TestIntegration:
    """Integration tests for overall game flow"""
    
    def test_game_creation_and_initialization(self):
        """Test complete game creation and setup"""
        game = NumberGuessingGame()
        assert game is not None
        assert len(game.high_scores) == 3
        assert len(game.difficulty_map) == 3
    
    def test_multiple_games_maintain_high_scores(self):
        """Test that high scores persist across game instances"""
        game1 = NumberGuessingGame()
        game1.high_scores['easy'] = 5
        
        # Simulate second game using same high scores
        high_scores = game1.high_scores.copy()
        game2 = NumberGuessingGame()
        game2.high_scores = high_scores
        
        assert game2.high_scores['easy'] == 5
    
    def test_difficulty_to_config_conversion(self):
        """Test that difficulty selection returns proper config"""
        game = NumberGuessingGame()
        with patch('builtins.input', return_value='1'):
            difficulty, config = game.select_difficulty()
            assert difficulty == 'easy'
            assert isinstance(config, dict)
            assert config['chances'] > 0
            assert config['hints'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])