# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When I guess lower than the secret number, it said to go higher. When I guess higher than the secret number, it said to go lower. 
The game starts off with 7 attempts and when I hate refresh, it starts off with 8 attempts. 
When I click start new game, it doesn't do anything, it is still showing the same message "Game over. Start a new game to try again."
It shows "out of attempts" when there is 1 attempt left


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

For this project, I used claude code. The AI provided many great suggestions that were correct including the hint being inversed. The ai did not provide any suggestions that were incorrect.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

The way i decided that a bug was really fixed is testing it on streamlit. One of the test I ran is the game starting at 1 less attempt than the expected, after making changes to the state, it showed the correct attempts left. Ai helped with finding exactly where the error was at and it provided a solution without asking.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number did not change for me. The rerun sessions basically resets everything back to 0, it's like you uninstall the app and you reinstall it. No change was necessary to gave the game a stable secret number

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

one habit from this project that I want to reuse in future labs or projects are understanding the errors first and knowing when to trust ai's outputs. Also, making the ai agent write test cases. One thing I would do differently is breaking down the tasks so that the ai agent can focus on one thing at a time. This project shows me the potential of ai and how it can be useful in many ways. I've used AI a lot and I am still learning how to use it as a tool more efficiently.