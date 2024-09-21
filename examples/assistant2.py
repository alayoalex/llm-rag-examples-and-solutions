import ollama

convo = []

while True:
    user_input = input('\nUSER: ')
    convo.append({'role': 'user', 'content': user_input})
    output = ollama.chat(model='llama3.1', messages=convo)
    response = output['message']['content']
    print(f'\nASSISTANT: \n{response} \n')
    convo.append({'role': 'assistant', 'content': response})
