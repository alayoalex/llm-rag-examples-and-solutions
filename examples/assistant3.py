import ollama

convo = []

def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='llama3.1', messages=convo, stream=True)
    print('\nASSISTANT:')

    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(content, end='', flush=True)

    print('\n')
    convo.append({'role': 'assistant', 'content': response})


while True:
    prompt = input('\nUSER: ')
    stream_response(prompt=prompt)
