from openai import OpenAI
client = OpenAI()


# Put Your API Key

# ----------------------------------------------------------------
# Coded by: Abdullah Alqurashi.
# ----------------------------
# Git-Hub: https://github.com/Kaser2023
# Linked-In: https://www.linkedin.com/in/abdullah-alqurashi-a3777a224/
# Date: 18.Rabi'a Alakhir. 1446 -  2024.Oct.21
# ----------------------------------------------------------------


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)