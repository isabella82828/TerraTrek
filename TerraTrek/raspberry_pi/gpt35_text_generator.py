key = "OPEN_AI_KEY"

import openai
openai.api_key = key


import random

def generate_fact(location):
  prompt = "Give a randomized short and interesting fact about the location {}, {}".format(location, random.randint(1, 1000))
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": prompt}
    ]
  )
  print(completion.choices[0].message.content)

  return completion.choices[0].message.content