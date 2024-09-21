import ollama
import chromadb

client = chromadb.Client()

message_history = [
    {
        'id': 1,
        'prompt': 'What is my name?',
        'response': 'Your name is Alexei Alayo. People call you Alex or Alayo.'
    },
    {
        'id': 2,
        'prompt': 'What is the square root of 144?',
        'response': '12'
    },
    {
        'id': 3,
        'prompt': 'What kind of dog do I have?',
        'response': 'You don\'t have a dog.'
    }
]
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

def create_vector_db(conversations):
    vector_db_name = 'conversations'
    try:
        client.delete_collection(name=vector_db_name)
    except: ValueError:
        pass

    vector_db = client.create_collection(name=vector_db_name)

    for c in conversations:
        serialized_convo = f'prompt: {c["prompt"]}, response: {c["response"]}'
        response = ollama.embeddings(model='nomic-embed-text', prompt=serialized_convo)
        embedding = response['embedding']

        vector_db.add(
            ids=[str(c['id'])],
            embeddings=[embedding],
            documents=[serialized_convo]
        )

def retrieve_embedding(prompt):
    response = ollama.embeddings(model='nomic-embed-text', prompt=prompt)
    prompt_embedding = response['embedding']

    vector_db = client.get_collection(name='conversations')
    results = vector_db.query(query_embedding=[prompt_embedding], n_results=1)
    best_embedding = results['embeddings'][0][0]

    return best_embedding

create_vector_db(conversations=message_history)

while True:
    prompt = input('\NUSER: \n')
    context = retrieve_embedding(prompt=prompt)
    prompt = f'USER PROMPT: {prompt} \nCONTEXT FROM EMBEDDING: {context}'
    stream_response(prompt=prompt)
