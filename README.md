# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

An AI wrote a "Number Guessing Game" in Streamlit, declared it production-ready, and left.
The game was unplayable:

- The hints lied — "Go HIGHER" when you should go lower.
- Hard mode was easier than Normal.
- Typing garbage wasted one of your attempts.
- Decimals slipped through silently.

This project documents finding every glitch, fixing them, and using the Claude API to explain *why* one of the bugs was wrong — not just that it was wrong.

---

## 🛠️ Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

To run the standalone AI explanation script:

```bash
python3 explain_glitch.py
```

> Requires an `ANTHROPIC_API_KEY` environment variable set in your shell for any Claude API features.

---

## 📝 Document Your Experience

### What is this game?

A number-guessing game with three difficulty levels. On each difficulty, the game picks a secret number within a range and gives you a limited number of attempts to guess it. After each guess, you get a hint: higher or lower. The goal is to find the number before you run out of attempts.

The "Game Glitch Investigator" section at the bottom of the app demonstrates using the Claude API to explain Bug 1's logic in plain language.

---

### Bugs Found

| # | Bug | Location |
|---|-----|----------|
| 1 | Hard difficulty range was 1–50, making it **easier** than Normal (1–100) | `app.py:9` |
| 2 | Hints were **backwards** — "Go HIGHER" when too high, "Go LOWER" when too low | `app.py:38-39` |
| 3 | Decimal inputs (e.g. `3.7`) were **silently rounded** to `3` and accepted | `app.py:22` |
| 4 | Invalid input (strings, decimals, blanks) **consumed an attempt** before validation ran | `app.py:147` |

---

### Fixes Applied

**Bug 1 — Hard range too small**

Hard mode used `1–50`. Normal used `1–100`. A smaller range = fewer possible values = easier to guess. Fixed by changing Hard's range to `1–500`.

```python
# Before
if difficulty == "Hard":
    return 1, 50

# After
if difficulty == "Hard":
    return 1, 500
```

---

**Bug 2 — Backwards hints**

The comparison was correct (`guess > secret` → "Too High") but the hint strings were swapped, sending players the wrong direction every time.

```python
# Before
if guess > secret:
    return "Too High", "📈 Go HIGHER!"
else:
    return "Too Low", "📉 Go LOWER!"

# After
if guess > secret:
    return "Too High", "📉 Go LOWER!"
else:
    return "Too Low", "📈 Go HIGHER!"
```

---

**Bug 3 — Decimals accepted silently**

The original code used `int(float(raw))` which converted `3.7` → `3` without any feedback. Fixed by explicitly rejecting any input that contains a `.` before conversion.

```python
if "." in raw:
    return False, None, "Please enter a whole number, not a decimal."
```

---

**Bug 4 — Attempt counter incremented before validation**

The attempt counter fired unconditionally when "Submit" was clicked, before `parse_guess` had a chance to reject bad input. Moved the increment inside the `else` block so it only runs on a valid guess.

```python
# Before
st.session_state.attempts += 1
ok, guess_int, err = parse_guess(raw_guess)
if not ok:
    st.error(err)

# After
ok, guess_int, err = parse_guess(raw_guess)
if not ok:
    st.error(err)
else:
    st.session_state.attempts += 1
```

---

### How We Got There

1. **Ran the game first** — got it live so bugs could be seen in context, not just in code
2. **Read the source top to bottom** — went through `app.py` line by line before touching anything
3. **Listed all bugs upfront** — catalogued issues before fixing any of them
4. **Used AI to explain Bug 1** — called Claude via the API to explain *why* a smaller range makes a game easier, framing the problem for a beginner audience
5. **Fixed one at a time** — addressed bugs individually, keeping changes small and reviewable

---

### What I Learned About AI-Assisted Debugging

**Where AI helped:**
- Explaining the *reasoning* behind a bug, not just pointing at the line
- Translating logic errors into plain language ("a smaller range means fewer guesses, so probability of a random guess being close is higher")
- Streaming responses made the explanation feel like a conversation, not a lookup

**Where human judgment still mattered:**
- AI doesn't play the game — identifying *which* bugs to investigate required running the app and experiencing the brokenness
- Deciding the correct fix required understanding intent, not just symptoms
- Verifying fixes actually worked meant running the app again, not trusting a static analysis

**Key takeaway:** AI is most useful when you already understand the problem well enough to ask a precise question. Asking "explain why this is wrong" gets better results than asking "find the bug."

---

## 📸 Demo

> Add a screenshot of your fixed, winning game below. Run `streamlit run app.py`, win a round, then drop the image here.

![Winning game screenshot](screenshots/winning_game.png)

---

## 🧪 Challenge 1: Pytest Results

The tests in `tests/test_game_logic.py` import `check_guess` from `logic_utils.py`. To make these pass, implement the function stubs in `logic_utils.py` by refactoring the logic out of `app.py`.

Run tests with:

```bash
python3 -m pytest tests/ -v
```

> Add a screenshot of your passing pytest output below once `logic_utils.py` is implemented.

![pytest results](screenshots/pytest_results.png)

---

## 🚀 Stretch Features

> If you completed Challenge 4 (Enhanced Game UI), add a screenshot here.

![Enhanced UI screenshot](screenshots/enhanced_ui.png)

---

## Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit game (fixed) |
| `logic_utils.py` | Stub functions for Challenge 1 refactor |
| `explain_glitch.py` | Standalone Claude API script — explains Bug 1 via streaming + extended thinking |
| `tests/test_game_logic.py` | Pytest tests for `check_guess` |
| `requirements.txt` | Dependencies |
