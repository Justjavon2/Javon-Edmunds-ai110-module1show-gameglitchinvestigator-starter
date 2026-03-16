from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_hints_not_backwards():
    # Regression: hints were previously reversed — a too-high guess incorrectly
    # displayed "Go HIGHER" and a too-low guess displayed "Go LOWER".
    # Verify the fix: guess 75 > secret 50 must return "Too High" (not "Too Low").
    assert check_guess(75, 50) == "Too High"
    assert check_guess(25, 50) == "Too Low"
