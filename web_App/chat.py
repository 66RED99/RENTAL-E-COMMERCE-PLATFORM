import openai

openai.api_key = "enteryourapikeyhere"
st=input()
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": st}])
print(completion.choices[0].message.content)