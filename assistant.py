import ollama

output = ollama.generate(model='llama3', prompt='hello world')
response = output['response']

print(response)
