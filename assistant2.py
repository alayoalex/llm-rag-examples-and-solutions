import ollama

convo = []

while True:
    user_input = input('You: ')
    convo.append({'role': 'user', 'content': user_input})
    output = ollama.chat(model='llama3.1', messages=convo)
    response = output['response']['content']
    print('Assistant: \n{response} \n')
    convo.append({'role': 'assistant', 'content': response})