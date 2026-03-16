# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

---

## 2. How did you use AI as a teammate?

I used Claude (via the Anthropic API directly in the app and via Claude Code in the terminal) as the primary AI tool throughout this project. I also used GitHub Copilot for in-editor suggestions while editing `logic_utils.py` and the test file.

**Correct suggestion:** When I asked Claude to explain why Hard difficulty with a range of 1–50 was wrong, it correctly explained the probability argument — with only 50 possible values, every guess eliminates a larger percentage of candidates, so it is statistically easier than Normal's 1–100 range. I verified this by changing the range to 1–500 and playing both difficulties back-to-back in the live app; Hard now clearly requires more attempts to converge on the answer.

**Incorrect or misleading suggestion:** The auto-generated docstring for `check_guess` in `logic_utils.py` said it should return `(outcome, message)` — a tuple — which matched `app.py`'s version. But the existing test file expected it to return just the outcome string (`"Win"`, `"Too High"`, `"Too Low"`). Following the docstring would have caused all three tests to fail with a type mismatch. I caught this by reading both files side-by-side before implementing the function, and implemented it to match what the tests actually asserted rather than what the AI-written docstring described.

---

## 3. Debugging and testing your fixes

For each fix, I used two layers of verification: a pytest unit test to confirm the logic in isolation, and the live Streamlit app to confirm the fix felt correct as a player. A passing test that covers the wrong behavior is useless, so running the app after every fix was non-negotiable.

The most targeted test was `test_hints_not_backwards` in `tests/test_game_logic.py`. It calls `check_guess(75, 50)` and asserts the result is `"Too High"`, and calls `check_guess(25, 50)` and asserts `"Too Low"`. Before the fix, the hint strings were swapped, meaning a too-high guess would display "Go HIGHER" — this test would have caught that immediately. Running `pytest tests/ -v` showed all 4 tests passing, confirming both the original starter tests and the new regression test were green.

Claude helped design the regression test by suggesting the pattern: pick a clear, unambiguous pair of values (75 vs 50, 25 vs 50) where the expected outcome is obvious, then assert the outcome name — not the display message — so the test stays stable even if the emoji wording changes later. That distinction between testing the outcome label versus the human-readable hint string was a useful framing I wouldn't have thought to make explicit on my own.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
