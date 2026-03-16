import anthropic

client = anthropic.Anthropic()

glitch_code = """
def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50     # <-- the glitch is here
    return 1, 100
"""

prompt = f"""
In a number guessing game, I found this glitch in the difficulty range logic:

{glitch_code}

The game has three difficulty levels — Easy, Normal, and Hard.
The expected behavior is that harder difficulties should be MORE challenging.

Explain:
1. What is wrong with the Hard difficulty range (1 to 50)?
2. Why does a smaller range actually make the game EASIER, not harder?
3. What range would actually make Hard mode harder than Normal?

Keep the explanation clear and concise, as if explaining to a beginner.
"""

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": prompt}]
) as stream:
    print("=== Claude's Explanation of the Hard Difficulty Glitch ===\n")
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print("\n")
