import openai

openai.api_key = "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"
st=input()
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": st}])
print(completion.choices[0].message.content)