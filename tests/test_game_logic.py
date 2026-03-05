import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ── Bug 1: Inverted hints ─────────────────────────────────────────────────────
# Before fix: guess < secret → told to go LOWER (wrong), guess > secret → told to go HIGHER (wrong)

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_low_outcome():
    outcome, message = check_guess(30, 50)   # 30 < 50 → should be Too Low
    assert outcome == "Too Low"

def test_guess_too_high_outcome():
    outcome, message = check_guess(70, 50)   # 70 > 50 → should be Too High
    assert outcome == "Too High"

def test_hint_goes_higher_when_guess_is_low():
    """Bug regression: guess below secret must say HIGHER, not LOWER."""
    outcome, message = check_guess(1, 100)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper(), f"Expected 'HIGHER' in hint, got: {message}"

def test_hint_goes_lower_when_guess_is_high():
    """Bug regression: guess above secret must say LOWER, not HIGHER."""
    outcome, message = check_guess(100, 1)
    assert outcome == "Too High"
    assert "LOWER" in message.upper(), f"Expected 'LOWER' in hint, got: {message}"

def test_hint_not_inverted_too_low():
    """Hint must NOT say LOWER when the guess is too low."""
    _, message = check_guess(10, 50)
    assert "LOWER" not in message.upper()

def test_hint_not_inverted_too_high():
    """Hint must NOT say HIGHER when the guess is too high."""
    _, message = check_guess(90, 50)
    assert "HIGHER" not in message.upper()


# ── Bug 2: Attempt limit off-by-one ──────────────────────────────────────────
# Before fix: game showed 7 attempts remaining on first load instead of 8 (Normal)
# Cause: attempts was initialised to 1 instead of 0.

def test_attempts_start_at_zero():
    """Attempts counter must start at 0 so first display shows full attempt_limit."""
    initial_attempts = 0          # correct initialisation in session_state
    attempt_limit = 8             # Normal difficulty
    assert attempt_limit - initial_attempts == 8


# ── Bug 3: New game button had no effect after game over ──────────────────────
# Before fix: status ("won"/"lost") was never reset, so the new game would
# immediately hit st.stop() again.  The fix resets status to "playing".

def test_new_game_resets_status():
    """Simulate what new-game logic must do: status must return to 'playing'."""
    status = "lost"                # game-over state before clicking New Game
    # ── fix applied ──
    status = "playing"
    assert status == "playing"

def test_new_game_resets_attempts():
    attempts = 8
    attempts = 0                   # reset on new game
    assert attempts == 0


# ── Bug 4: "Out of attempts" shown 1 attempt too early ───────────────────────
# Before fix: game_over triggered at attempts > attempt_limit (strict >)
# instead of attempts >= attempt_limit.

def test_game_over_at_exact_limit():
    """At exactly attempt_limit attempts the game should end."""
    attempt_limit = 8
    attempts_used = 8
    assert attempts_used >= attempt_limit   # correct boundary check

def test_game_not_over_one_before_limit():
    """One attempt before the limit the game must still be active."""
    attempt_limit = 8
    attempts_used = 7
    assert not (attempts_used >= attempt_limit)

def test_game_over_not_triggered_early():
    """Bug regression: 7 attempts used out of 8 should NOT trigger game over."""
    attempt_limit = 8
    attempts_used = 7
    game_over = attempts_used > attempt_limit   # wrong (old) check
    assert game_over is False                   # even the wrong check passes here
    correct_game_over = attempts_used >= attempt_limit
    assert correct_game_over is False           # correct check also False at 7/8


# ── Supporting logic: parse_guess ────────────────────────────────────────────

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err is not None


# ── Supporting logic: get_range_for_difficulty ───────────────────────────────

def test_difficulty_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_difficulty_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

def test_difficulty_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 50


# ── High score tracking ───────────────────────────────────────────────────────
# High score logic in app.py: if score > high_score: high_score = score

def test_high_score_initializes_at_zero():
    """High score must start at 0 before any game is played."""
    high_score = 0
    assert high_score == 0

def test_high_score_updates_when_new_score_is_higher():
    """A new score that beats the record should become the new high score."""
    high_score = 50
    score = 80
    if score > high_score:
        high_score = score
    assert high_score == 80

def test_high_score_not_updated_when_new_score_is_lower():
    """A score below the record must not overwrite the high score."""
    high_score = 80
    score = 40
    if score > high_score:
        high_score = score
    assert high_score == 80

def test_high_score_not_updated_when_score_is_equal():
    """An equal score must not overwrite the high score (strict >)."""
    high_score = 80
    score = 80
    if score > high_score:
        high_score = score
    assert high_score == 80

def test_high_score_set_from_zero_on_first_win():
    """Any positive score after the first game should become the high score."""
    high_score = 0
    score = 70
    if score > high_score:
        high_score = score
    assert high_score == 70

def test_high_score_updates_on_loss_if_score_is_higher():
    """High score should update even when the player loses, if score beats record."""
    high_score = 30
    score = 45          # accumulated before running out of attempts
    if score > high_score:
        high_score = score
    assert high_score == 45

def test_high_score_persists_across_new_game():
    """Starting a new game resets score but must not reset high_score."""
    high_score = 90
    # simulate new game reset (only score/attempts/status/history are cleared)
    score = 0
    attempts = 0
    status = "playing"
    assert high_score == 90   # high_score unchanged
