import ollama

convo = []

def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='llama3.1', messages=convo, stream=True)
    print('Assistant:')

    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(content, end='', flush=True)

    print('\n')
    convo.append({'role': 'assistant', 'content': response})


while True:
    prompt = input('You: ')
    stream_response(prompt=prompt)
